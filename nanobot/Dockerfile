# Multi-stage build for nanobot gateway service
# Uses uv for dependency management

# ---
# Stage 1: Build the application in the `/app/nanobot` directory
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads, use system interpreter
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
# Copy workspace root files for workspace dependency resolution
COPY --from=workspace pyproject.toml uv.lock /app/
# Copy mcp directory from workspace
COPY --from=workspace mcp /app/mcp
# Copy nanobot-websocket-channel from workspace for nanobot-webchat
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel
COPY pyproject.toml /app/nanobot/pyproject.toml

COPY . /app/nanobot

# First sync without workspace deps
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

COPY . /app/nanobot

# Install nanobot-webchat directly into the venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python /app/.venv/bin/python 'nanobot-webchat @ file:///app/nanobot-websocket-channel/nanobot-webchat'

# Install uv and mcp-lms for MCP server support
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python /app/.venv/bin/python uv 'lms-mcp @ file:///app/mcp'

# ---
# Stage 2: Final runtime image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/nanobot"

# Use the non-root user
USER nonroot

WORKDIR /app

# Run the nanobot gateway via our entrypoint script
CMD ["python", "/app/nanobot/entrypoint.py"]
