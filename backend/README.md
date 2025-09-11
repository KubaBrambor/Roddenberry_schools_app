# FastAPI Starter

Look at the [FastAPI documentation](https://fastapi.tiangolo.com) to learn more.

## Setup

### Setup for [uv](https://docs.astral.sh/uv/) users

```bash
# Install dependencies
uv sync
```

### Setup for [pip](https://pip.pypa.io/en/stable/getting-started/) users

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install .
```

## Database Configuration

### PostgreSQL Environment Variables

Set PostgreSQL credentials in `app/core/.env`, format:

```ini
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_SERVER=
POSTGRES_PORT=
POSTGRES_DB=
```

## Running the Project

### You can run backend with FastAPI

- for pip users

```bash
fastapi dev main.py
```

- for uv users

```bash
uv run fastapi dev
```

### Or with Uvicorn directly

- for pip users

```bash
uvicorn main:app --reload
```

- for uv users

```bash
uv run uvicorn main:app --reload
```
