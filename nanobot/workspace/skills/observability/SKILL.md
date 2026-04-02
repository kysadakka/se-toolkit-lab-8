# Observability Skill

You have access to observability tools that let you query logs and traces from the LMS system.

## Available Tools

### Log Tools (VictoriaLogs)

- **`logs_search`** — Search logs using LogsQL queries
  - Use `query="*"` for all recent logs
  - Use `query="severity:ERROR"` for errors only
  - Use `query="event:request_completed"` for completed requests
  - Use `query="service.name=\"backend\""` for backend-specific logs
  - Default limit is 20 entries

- **`logs_error_count`** — Count errors per service
  - Use when user asks about "errors", "problems", "what went wrong"
  - Default time window is 60 minutes
  - Returns count grouped by service name

### Trace Tools (VictoriaTraces)

- **`traces_list`** — List recent traces for a service
  - Shows trace ID, span count, duration, and service
  - Use to see recent request patterns

- **`traces_get`** — Fetch a specific trace by ID
  - Use when you have a `trace_id` from logs
  - Shows the full span hierarchy and timing
  - Helps identify which step in a request failed

## Strategy

### When user asks "What went wrong?" or "Check system health"

1. **First**, call `logs_error_count(minutes=5)` to see recent errors
2. **Then**, call `logs_search(query="severity:ERROR", limit=10)` to see error details
3. **Look for** `trace_id` in the error log entries
4. **If** you find a `trace_id`, call `traces_get(trace_id="...")` to see the full trace
5. **Summarize** findings concisely:
   - What service failed
   - What error occurred
   - When it happened
   - Root cause from trace analysis
   - Don't dump raw JSON

### When user asks about errors

1. **First**, call `logs_error_count` to see which services have errors
2. **Then**, call `logs_search` with `query="severity:ERROR"` to see error details
3. **If** you find a `trace_id` in the error logs, call `traces_get` to see the full trace
4. **Summarize** findings concisely — don't dump raw JSON

### When user asks about a specific request

1. **Search** logs with `logs_search` using relevant keywords
2. **Find** the `trace_id` from the log entry
3. **Fetch** the full trace with `traces_get`
4. **Explain** what happened in the request flow

### When debugging a failure

1. **Check** error count: `logs_error_count(minutes=30)`
2. **Search** recent errors: `logs_search(query="severity:ERROR", limit=10)`
3. **Look for** patterns: same service, same error type, same time
4. **Fetch** traces if trace IDs are available
5. **Report** root cause: which service failed, why, and when

## Response Format

- Keep responses concise and actionable
- Summarize findings, don't dump raw JSON
- Highlight the most important information first
- Include timestamps when relevant
- Suggest next steps if appropriate

## Examples

**User:** "What went wrong?"

**You:**
1. Call `logs_error_count(minutes=5)`
2. Call `logs_search(query="severity:ERROR", limit=10)`
3. Extract `trace_id` from error logs
4. Call `traces_get(trace_id="...")`
5. Summarize: "The backend service failed at 10:30 AM with a database connection error. The trace shows the request failed at the `db_query` span after 30s timeout. Root cause: PostgreSQL was unavailable..."

**User:** "Any errors in the last hour?"

**You:**
1. Call `logs_error_count(minutes=60)`
2. If errors found, call `logs_search(query="severity:ERROR", limit=10)`
3. Summarize: "Found 15 errors in the last hour. Most are from the backend service (12 errors) related to database connection failures..."

**User:** "What happened with request XYZ?"

**You:**
1. Call `logs_search(query="XYZ", limit=10)`
2. Find trace_id in results
3. Call `traces_get(trace_id="...")` 
4. Summarize: "The request started at 10:30 AM, went through authentication (5ms), then failed at database query (timeout after 30s)..."

**User:** "Show me recent activity"

**You:**
1. Call `logs_search(query="*", limit=20)`
2. Summarize: "Recent activity shows 18 successful requests and 2 errors. The errors occurred at 10:45 AM when the backend couldn't connect to PostgreSQL..."
