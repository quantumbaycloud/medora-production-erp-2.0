# Common Utilities

A drop-in FastAPI module implementing four shared services:

| Utility | What it does |
|---|---|
| **Error Logs** | Captures application errors (manually via API, or automatically for any unhandled exception) with stack traces, stored in DB + `app/logs/error.log` (JSON) |
| **Activity Logs** | Records who did what — automatically logs every HTTP request (method, path, status, IP, duration) via middleware, plus a manual API for custom events |
| **System Logs** | For background jobs / infra-level events (startup, scheduled tasks, etc.) |
| **Health Check** | `GET /health` — checks DB connectivity, disk space, memory, and CPU; returns `healthy` / `degraded` / `unhealthy` |

## Project structure

Everything lives in one flat folder — no nested packages:

```
common_utilities/
├── main.py            # FastAPI app + all routes
├── models.py          # SQLAlchemy tables: ErrorLog, ActivityLog, SystemLog
├── schemas.py          # Pydantic request/response schemas
├── database.py         # DB engine/session (SQLite by default)
├── logging_config.py   # Rotating JSON file loggers
├── middleware.py        # Auto-logs every request as an ActivityLog
├── health.py            # Health check logic
├── logs/                # Rotating .log files + SQLite DB land here at runtime
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Interactive API docs: **http://localhost:8000/docs**

By default it uses a local SQLite file (`logs/common_utilities.db`).
For production, set an env var before starting:

```bash
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Run the health check |
| POST / GET | `/logs/errors` | Record / query error logs |
| POST / GET | `/logs/activity` | Record / query activity logs |
| POST / GET | `/logs/system` | Record / query system logs |

Query params on the GET endpoints let you filter (`level`, `source`, `user_id`, `action`, `component`) and set `limit` (default 50, max 500).

## How it plugs into an existing app

- **Errors**: any unhandled exception in the app is caught automatically by the global exception handler and logged — no extra code needed. To log a handled error explicitly, `POST /logs/errors` or import `error_logger` from `logging_config` directly.
- **Activity**: every request is logged automatically by `ActivityLoggingMiddleware`. To attach a user ID, set `request.state.user_id` in your auth dependency before the middleware runs.
- **System**: call `POST /logs/system`, or import `system_logger` / `log_with_extra` from `logging_config` inside cron jobs, startup/shutdown hooks, etc.
- **Health Check**: point your load balancer / uptime monitor at `GET /health`. It returns HTTP 200 regardless of status — check the `status` field in the JSON body (`healthy`/`degraded`/`unhealthy`) rather than the HTTP code, since some infra treats non-200 as "restart the container."

## Notes

- Logs are stored in two places: the database (for structured querying via the API) and rotating JSON files in `app/logs/` (5MB per file, 5 backups) as a durable fallback if the DB is down.
- Extend the thresholds in `app/health.py` (`DISK_WARN_PCT`, `MEMORY_WARN_PCT`, `CPU_WARN_PCT`) to match your infra's SLAs.
- This is a self-contained demo service. If you already have a FastAPI app, the cleanest integration is copying `logging_config.py`, `middleware.py`, `health.py`, and the relevant `models.py` classes into your existing app rather than running this as a separate service.
