# Task Management

A simple FastAPI + SQLModel task-management API backed by SQLite.

- **Python**: >= 3.14
- **Package manager**: `uv`
- **HTTP framework**: FastAPI
- **ORM**: SQLModel

# Why this project matters

This project demonstrates REST API design, relational data modeling, 
route protection with API keys, task lifecycle management, pagination, 
and background processing with FastAPI.

## Badges
[![wakatime](https://wakatime.com/badge/user/b14e5466-6c05-4b34-9f02-6af1d1142376/project/5f8c7e71-fbf1-44a8-88c9-7bf989afb3af.svg)](https://wakatime.com/badge/user/b14e5466-6c05-4b34-9f02-6af1d1142376/project/5f8c7e71-fbf1-44a8-88c9-7bf989afb3af)


## Setup

```bash
uv sync          # install dependencies
uv run uvicorn main:app --reload   # run the dev server
```

Interactive docs are available at `http://localhost:8000/docs`.

## How it works

On startup, `main.py` calls `create_db_and_tables()`, which auto-creates any missing tables in the SQLite database at `database_file.db`.

> There is no migration tooling. If you change a table model, delete `database_file.db` before restarting so the new schema is created.

## API

### Users — no auth required

| Method | Endpoint       | Description              |
| ------ | -------------- | ------------------------ |
| POST   | `/user/`       | Create a user            |

`POST /user/` body:

```json
{ "username": "alice", "email": "alice@example.com", "age": 30 }
```

`age` must be `>= 16` and `< 85`. `email` is the primary key, so a duplicate email returns `400`.

### Tasks — require `X-API-Key` header

All `/task` routes require an `X-API-Key` header. Set the expected key through the `TASK_API_KEY` environment variable.

```
X-API-Key: replace-with-your-api-key
```

| Method | Endpoint                    | Description                          |
| ------ | --------------------------- | ------------------------------------ |
| POST   | `/task/?user_id={email}`    | Create a task for a user             |
| GET    | `/task/?skip=0&limit=10`    | List tasks (paginated)               |
| PUT    | `/task/{task_id}`           | Update a task                        |
| PATCH  | `/task/{task_id}/status?status={status}` | Update a task's status     |
| DELETE | `/task/{task_id}`           | Delete a task                        |

`POST /task/` body (status is `todo`, `in_progress`, or `done`):

```json
{ "title": "Ship feature", "description": "Finish the feature", "status": "todo" }
```

- `user_id` must be an existing user's email, otherwise `POST /task/` returns `404`.
- When a task transitions to `done`, the app logs the completion to `report.log` (via a FastAPI `BackgroundTasks` hook).

## Runtime artifacts

The following files are produced at runtime and should not be committed:

- `database_file.db` — SQLite database
- `report.log` — task completion log
