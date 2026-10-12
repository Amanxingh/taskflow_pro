# TaskFlow Pro — Python Task Management API

A structured FastAPI project for managing tasks. Includes CRUD endpoints, filtering, search, pagination, validation, automated tests, environment configuration, Docker, and Docker Compose.

## Features

- Create, list, read, update, and delete tasks
- Search task titles and descriptions
- Filter by completion status and priority
- Paginated task listing
- Request validation with Pydantic
- SQLAlchemy ORM with SQLite persistence
- Interactive API docs
- Automated tests with pytest
- Docker image and Compose setup
- Health endpoint and container health check

## Project structure

```text
taskflow_pro/
├── app/
│   ├── api/routes.py
│   ├── core/config.py
│   ├── db/session.py
│   ├── models/task.py
│   ├── schemas/task.py
│   ├── services/task_service.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
├── data/                  # Created automatically; ignored by Git
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Run locally on Windows

Open this folder in VS Code, then run the following in the terminal.

### 1. Create a virtual environment

```bash
python -m venv myenv
```

### 2. Activate it in Git Bash

```bash
source myenv/Scripts/activate
```

PowerShell alternative:

```powershell
.\myenv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/v1/health

The SQLite database is created under `data/taskflow.db`.

## Run with Docker

Make sure Docker Desktop is running, then from the project root:

```bash
docker compose up --build -d
```

Check containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f api
```

Stop the project:

```bash
docker compose down
```

Stop and remove the persistent database volume too (this permanently deletes stored tasks):

```bash
docker compose down -v
```

## Run tests

```bash
pytest -v
```

## API endpoint guide

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome information |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/tasks` | Create a task |
| GET | `/api/v1/tasks` | List, search, and filter tasks |
| GET | `/api/v1/tasks/{task_id}` | Get one task |
| PATCH | `/api/v1/tasks/{task_id}` | Update task fields |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task |

### Example: create a task

Send a POST request to `/api/v1/tasks` with JSON:

```json
{
  "title": "Learn Docker",
  "description": "Build an image and run a container",
  "priority": "high",
  "due_date": null
}
```

### Example: list and filter

```text
GET /api/v1/tasks?q=docker&completed=false&priority=high&skip=0&limit=10
```

Valid priorities: `low`, `medium`, `high`.

## Git and GitHub setup

Create a new, empty repository on GitHub, then run:

```bash
git init
git add .
git commit -m "Initial commit: TaskFlow Pro API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

If Git is already initialized and has a remote, do not repeat `git init` or `git remote add origin`; inspect with `git status` and `git remote -v` first.

## Notes

- `.env.example` documents environment settings. Copy it to `.env` if you want local overrides; `.env` is ignored by Git.
- SQLite is chosen to make local setup straightforward. For a multi-user production deployment, consider PostgreSQL, database migrations (Alembic), authentication, and deployment-specific secret management.
- This is a learning project with a production-style layout, not a fully production-hardened service.
