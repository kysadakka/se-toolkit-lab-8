# Cron Skill — Scheduled Tasks

You have a built-in `cron` tool that lets you schedule reminders and recurring tasks. Jobs are tied to the current chat session — when they run, they post their message to the same chat where they were created.

## Available Actions

### `cron(action="add", message="...", every_seconds=...)` — Schedule a recurring task

Creates a job that runs repeatedly at a fixed interval.

**Parameters:**
- `message` (required) — What to post when the job runs
- `every_seconds` — Run every N seconds (e.g., `120` for every 2 minutes, `900` for every 15 minutes)

**Example:**
```
cron(action="add", message="Check for backend errors and post a summary", every_seconds=120)
```

### `cron(action="add", message="...", cron_expr="...", tz="...")` — Schedule at specific times

Creates a job that runs on a cron schedule (e.g., daily at 9 AM).

**Parameters:**
- `message` (required) — What to post when the job runs
- `cron_expr` — Cron expression like `"0 9 * * *"` (daily at 9 AM)
- `tz` (optional) — Timezone like `"Asia/Shanghai"` or `"UTC"`

**Common cron expressions:**
- `"*/15 * * * *"` — Every 15 minutes
- `"0 * * * *"` — Every hour at minute 0
- `"0 9 * * *"` — Daily at 9 AM
- `"0 9 * * 1"` — Every Monday at 9 AM

**Example:**
```
cron(action="add", message="Morning health check", cron_expr="0 9 * * *", tz="Asia/Shanghai")
```

### `cron(action="list")` — List scheduled jobs

Shows all jobs for the current session with their IDs, schedules, and last/next run times.

**Example:**
```
cron(action="list")
```

**Response format:**
```
Scheduled jobs:
- Health check (id: abc123, every 2m)
  Next run: 2026-04-02T10:32:00 (UTC)
- Daily report (id: def456, cron: 0 9 * * *)
  Last run: 2026-04-02T09:00:00 (UTC) — success
  Next run: 2026-04-03T09:00:00 (UTC)
```

### `cron(action="remove", job_id="...")` — Remove a job

Deletes a scheduled job by ID.

**Example:**
```
cron(action="remove", job_id="abc123")
```

## Strategy

### When user asks for a recurring/periodic task

1. **Clarify the interval** if not specified:
   - "How often should I run this? Every 15 minutes, hourly, daily?"
   
2. **Choose the right schedule type:**
   - Fixed interval (every N seconds/minutes) → use `every_seconds`
   - Specific times (daily at 9 AM) → use `cron_expr`

3. **Create the job:**
   ```
   cron(action="add", message="<what the user asked for>", every_seconds=<interval>)
   ```

4. **Confirm creation:**
   - "I've created a job that runs every 15 minutes. It will post a message to this chat each time."

### When user asks "List scheduled jobs" or "What jobs are running?"

1. Call `cron(action="list")`
2. Present the results in a readable format
3. If no jobs exist, say "No scheduled jobs yet."

### When user asks to cancel/remove a job

1. If they provide an ID: `cron(action="remove", job_id="...")`
2. If they don't: First call `cron(action="list")` to find the ID, then remove it
3. Confirm: "I've removed the health check job."

### Health check pattern (common use case)

When the user asks for a health check that runs periodically:

1. **Create the job:**
   ```
   cron(action="add", 
        message="Health check: check for backend errors in the last 2 minutes, inspect a trace if needed, and post a short summary. If no errors, say the system looks healthy.", 
        every_seconds=120)
   ```

2. **Explain what will happen:**
   - "I'll check for errors every 2 minutes and post a summary here. If there are no errors, I'll report that the system is healthy."

3. **When the job runs (proactive message):**
   - Call `logs_error_count(minutes=2)` to check for recent errors
   - If errors found: call `logs_search(query="severity:ERROR", limit=10)`, extract trace IDs, call `traces_get()` if available, summarize findings
   - If no errors: "System looks healthy — no errors in the last 2 minutes."

## Important Notes

1. **Jobs are session-bound** — A job created in one chat will post to that same chat. You can't create a job from chat A that posts to chat B.

2. **No nested scheduling** — You cannot create new jobs from within a cron job execution. If a job needs to schedule follow-ups, it must do so indirectly (e.g., by asking the user).

3. **Timezone handling:**
   - `every_seconds` always counts from "now" — no timezone needed
   - `cron_expr` uses the default timezone (UTC) unless you specify `tz`
   - Always include `tz` with `cron_expr` for clarity

4. **Short intervals for testing** — Use `every_seconds=120` (2 minutes) for testing. Remember to remove test jobs afterward.

5. **Job names are truncated** — The first 30 characters of the message become the job name for display.

## Examples

**User:** "Create a health check that runs every 15 minutes."

**You:**
1. Call `cron(action="add", message="Health check: check for backend errors and post a summary", every_seconds=900)`
2. Respond: "I've scheduled a health check that runs every 15 minutes. Each time it runs, I'll check for errors and post a summary to this chat."

---

**User:** "List scheduled jobs."

**You:**
1. Call `cron(action="list")`
2. Present the results clearly

---

**User:** "Remove the health check job."

**You:**
1. Call `cron(action="list")` to find the job ID
2. Call `cron(action="remove", job_id="<found_id>")`
3. Respond: "I've removed the health check job."

---

**User:** "Can you check for errors every 2 minutes and let me know?"

**You:**
1. Call `cron(action="add", message="Check for backend errors in the last 2 minutes and post a summary", every_seconds=120)`
2. Respond: "I'll check for errors every 2 minutes and post updates here."
