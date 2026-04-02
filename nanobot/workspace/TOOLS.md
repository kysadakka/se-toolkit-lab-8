# Tool Usage Notes

Tool signatures are provided automatically via function calling.
This file documents non-obvious constraints and usage patterns.

## exec — Safety Limits

- Commands have a configurable timeout (default 60s)
- Dangerous commands are blocked (rm -rf, format, dd, shutdown, etc.)
- Output is truncated at 10,000 characters
- `restrictToWorkspace` config can limit file access to the workspace

## cron — Scheduled Reminders

The `cron` tool is built into nanobot — you don't need to define it. It's automatically available when the agent starts.

**To use it:** Follow the guidance in `skills/cron/SKILL.md`.

**Key points:**
- Jobs are tied to the current chat session — they post back to the same chat where they were created
- Use `action="add"` with `every_seconds` for recurring tasks (e.g., every 2 minutes)
- Use `action="list"` to see scheduled jobs
- Use `action="remove"` with `job_id` to cancel a job
- The agent cannot create new jobs from within a cron job execution
