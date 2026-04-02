"""Stdio MCP server exposing LMS backend operations as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
import urllib.parse
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_lms.client import LMSClient

_base_url: str = ""

server = Server("lms")

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _NoArgs(BaseModel):
    """Empty input model for tools that only need server-side configuration."""


class _LabQuery(BaseModel):
    lab: str = Field(description="Lab identifier, e.g. 'lab-04'.")


class _TopLearnersQuery(_LabQuery):
    limit: int = Field(
        default=5, ge=1, description="Max learners to return (default 5)."
    )


class _LogsQuery(BaseModel):
    query: str = Field(
        default="*",
        description="LogsQL query string. Use '*' for all logs, 'severity:ERROR' for errors, 'event:request_completed' for completed requests.",
    )
    limit: int = Field(default=20, ge=1, le=1000, description="Max log entries to return (default 20).")


class _ErrorCountQuery(BaseModel):
    minutes: int = Field(
        default=60, ge=1, le=1440, description="Time window in minutes (default 60)."
    )


class _TracesQuery(BaseModel):
    service: str = Field(
        default="Learning Management Service",
        description="Service name to filter traces (default: 'Learning Management Service').",
    )
    limit: int = Field(default=10, ge=1, le=100, description="Max traces to return (default 10).")


class _TraceByIdQuery(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch (e.g., from logs).")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_api_key() -> str:
    for name in ("NANOBOT_LMS_API_KEY", "LMS_API_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    raise RuntimeError(
        "LMS API key not configured. Set NANOBOT_LMS_API_KEY or LMS_API_KEY."
    )


def _client() -> LMSClient:
    if not _base_url:
        raise RuntimeError(
            "LMS backend URL not configured. Pass it as: python -m mcp_lms <base_url>"
        )
    return LMSClient(_base_url, _resolve_api_key())


def _text(data: BaseModel | Sequence[BaseModel]) -> list[TextContent]:
    """Serialize a pydantic model (or list of models) to a JSON text block."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = [item.model_dump() for item in data]
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))]


# ---------------------------------------------------------------------------
# Observability helpers
# ---------------------------------------------------------------------------

_VICTORIALOGS_URL = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
_VICTORIATRACES_URL = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")


async def _victorialogs_query(query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Query VictoriaLogs using LogsQL."""
    async with httpx.AsyncClient() as client:
        url = f"{_VICTORIALOGS_URL}/select/logsql/query"
        params = {"query": query, "limit": limit}
        resp = await client.get(url, params=params, timeout=30.0)
        resp.raise_for_status()
        # VictoriaLogs returns newline-delimited JSON
        lines = resp.text.strip().split("\n")
        return [json.loads(line) for line in lines if line.strip()]


async def _victoriatraces_list(service: str, limit: int = 10) -> list[dict[str, Any]]:
    """List recent traces from VictoriaTraces (Jaeger API)."""
    async with httpx.AsyncClient() as client:
        url = f"{_VICTORIATRACES_URL}/jaeger/api/traces"
        params = {"service": service, "limit": limit}
        resp = await client.get(url, params=params, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", [])


async def _victoriatraces_get(trace_id: str) -> dict[str, Any]:
    """Fetch a specific trace by ID from VictoriaTraces."""
    async with httpx.AsyncClient() as client:
        url = f"{_VICTORIATRACES_URL}/jaeger/api/traces/{trace_id}"
        resp = await client.get(url, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        traces = data.get("data", [])
        return traces[0] if traces else {}


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _health(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().health_check())


async def _labs(_args: _NoArgs) -> list[TextContent]:
    items = await _client().get_items()
    return _text([i for i in items if i.type == "lab"])


async def _learners(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().get_learners())


async def _pass_rates(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_pass_rates(args.lab))


async def _timeline(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_timeline(args.lab))


async def _groups(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_groups(args.lab))


async def _top_learners(args: _TopLearnersQuery) -> list[TextContent]:
    return _text(await _client().get_top_learners(args.lab, limit=args.limit))


async def _completion_rate(args: _LabQuery) -> list[TextContent]:
    return _text(await _client().get_completion_rate(args.lab))


async def _sync_pipeline(_args: _NoArgs) -> list[TextContent]:
    return _text(await _client().sync_pipeline())


# ---------------------------------------------------------------------------
# Observability tool handlers
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsQuery) -> list[TextContent]:
    """Search logs using VictoriaLogs."""
    try:
        results = await _victorialogs_query(args.query, args.limit)
        # Summarize results
        if not results:
            return [TextContent(type="text", text="No logs found matching the query.")]
        
        # Count by severity
        severity_counts: dict[str, int] = {}
        for log in results:
            sev = log.get("severity", "UNKNOWN")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        summary = f"Found {len(results)} log entries.\n\n"
        summary += "Severity breakdown:\n"
        for sev, count in sorted(severity_counts.items(), key=lambda x: -x[1]):
            summary += f"  {sev}: {count}\n"
        summary += "\nRecent entries:\n"
        for log in results[:5]:
            ts = log.get("_time", "unknown")[:19]
            msg = log.get("_msg", "no message")[:100]
            sev = log.get("severity", "UNKNOWN")
            summary += f"  [{ts}] {sev}: {msg}\n"
        
        return [TextContent(type="text", text=summary)]
    except Exception as exc:
        return [TextContent(type="text", text=f"Error querying logs: {type(exc).__name__}: {exc}")]


async def _logs_error_count(args: _ErrorCountQuery) -> list[TextContent]:
    """Count errors per service over a time window."""
    try:
        # Query for ERROR severity logs
        query = f"severity:ERROR | stats by(service.name) count() | sort by count desc"
        results = await _victorialogs_query(query, limit=50)
        
        if not results:
            return [TextContent(type="text", text=f"No errors found in the last {args.minutes} minutes.")]
        
        summary = f"Error count in the last {args.minutes} minutes:\n\n"
        for log in results:
            service = log.get("service.name", "unknown")
            count = log.get("count", 0)
            summary += f"  {service}: {count} errors\n"
        
        return [TextContent(type="text", text=summary)]
    except Exception as exc:
        return [TextContent(type="text", text=f"Error counting logs: {type(exc).__name__}: {exc}")]


async def _traces_list(args: _TracesQuery) -> list[TextContent]:
    """List recent traces for a service."""
    try:
        traces = await _victoriatraces_list(args.service, args.limit)
        
        if not traces:
            return [TextContent(type="text", text=f"No traces found for service '{args.service}'.")]
        
        summary = f"Recent traces for '{args.service}':\n\n"
        summary += f"{'Trace ID':<36} {'Spans':<6} {'Duration':<12} {'Service'}\n"
        summary += "─" * 80 + "\n"
        
        for trace in traces[:10]:
            trace_id = trace.get("traceID", "unknown")[:36]
            spans = len(trace.get("spans", []))
            duration_us = trace.get("duration", 0)
            duration_ms = duration_us / 1000 if duration_us else 0
            if duration_ms > 1000:
                duration_str = f"{duration_ms/1000:.1f}s"
            else:
                duration_str = f"{duration_ms:.1f}ms"
            service = trace.get("serviceName", "unknown")
            summary += f"{trace_id:<36} {spans:<6} {duration_str:<12} {service}\n"
        
        return [TextContent(type="text", text=summary)]
    except Exception as exc:
        return [TextContent(type="text", text=f"Error listing traces: {type(exc).__name__}: {exc}")]


async def _traces_get(args: _TraceByIdQuery) -> list[TextContent]:
    """Fetch a specific trace by ID."""
    try:
        trace = await _victoriatraces_get(args.trace_id)
        
        if not trace:
            return [TextContent(type="text", text=f"Trace {args.trace_id} not found.")]
        
        summary = f"Trace {args.trace_id[:36]}:\n\n"
        duration_us = trace.get("duration", 0)
        duration_ms = duration_us / 1000 if duration_us else 0
        summary += f"Duration: {duration_ms:.1f}ms\n"
        summary += f"Spans: {len(trace.get('spans', []))}\n\n"
        summary += "Span hierarchy:\n"
        
        # Build span tree
        spans = trace.get("spans", [])
        span_map = {s["spanID"]: s for s in spans}
        
        def print_span(span_id: str, indent: int = 0) -> str:
            span = span_map.get(span_id)
            if not span:
                return ""
            name = span.get("operationName", "unknown")
            duration = span.get("duration", 0) / 1000  # to ms
            service = span.get("process", {}).get("serviceName", "unknown")
            result = f"  {'  ' * indent}• {name} ({duration:.1f}ms) [{service}]\n"
            
            # Find child spans
            for child in spans:
                if child.get("references", [{}])[0].get("refType") == "CHILD_OF" and \
                   child.get("references", [{}])[0].get("spanID") == span_id:
                    result += print_span(child["spanID"], indent + 1)
            
            return result
        
        # Find root spans (no parent or parent is self)
        for span in spans:
            refs = span.get("references", [])
            if not refs or refs[0].get("refType") != "CHILD_OF":
                summary += print_span(span["spanID"])
        
        return [TextContent(type="text", text=summary)]
    except Exception as exc:
        return [TextContent(type="text", text=f"Error fetching trace: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Registry: tool name -> (input model, handler, Tool definition)
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    # Pydantic puts definitions under $defs; flatten for MCP's JSON Schema expectation.
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (
        model,
        handler,
        Tool(name=name, description=description, inputSchema=schema),
    )


_register(
    "lms_health",
    "Check if the LMS backend is healthy and report the item count.",
    _NoArgs,
    _health,
)
_register("lms_labs", "List all labs available in the LMS.", _NoArgs, _labs)
_register(
    "lms_learners", "List all learners registered in the LMS.", _NoArgs, _learners
)
_register(
    "lms_pass_rates",
    "Get pass rates (avg score and attempt count per task) for a lab.",
    _LabQuery,
    _pass_rates,
)
_register(
    "lms_timeline",
    "Get submission timeline (date + submission count) for a lab.",
    _LabQuery,
    _timeline,
)
_register(
    "lms_groups",
    "Get group performance (avg score + student count per group) for a lab.",
    _LabQuery,
    _groups,
)
_register(
    "lms_top_learners",
    "Get top learners by average score for a lab.",
    _TopLearnersQuery,
    _top_learners,
)
_register(
    "lms_completion_rate",
    "Get completion rate (passed / total) for a lab.",
    _LabQuery,
    _completion_rate,
)
_register(
    "lms_sync_pipeline",
    "Trigger the LMS sync pipeline. May take a moment.",
    _NoArgs,
    _sync_pipeline,
)

# Observability tools
_register(
    "logs_search",
    "Search logs in VictoriaLogs using LogsQL. Use for debugging errors, finding specific events, or exploring recent activity.",
    _LogsQuery,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count errors per service over a time window. Use to identify which services are having problems.",
    _ErrorCountQuery,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces for a service. Shows trace ID, span count, duration, and service name.",
    _TracesQuery,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch a specific trace by ID. Shows the span hierarchy and timing for debugging request flows.",
    _TraceByIdQuery,
    _traces_get,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main(base_url: str | None = None) -> None:
    global _base_url
    _base_url = base_url or os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
