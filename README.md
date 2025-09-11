# Roddenberry_schools_app

This repository contains an app made by FujiTech students participating in a mentoring program.

🚀 The purpose of this repository is to showcase the group work of students participating in mentoring sessions, where they develop a complete application (frontend and backend). The application development is conducted under the guidance of a mentor, who is responsible for code review and organizing the workflow using the Scrum methodology (acting as the Scrum Master).

## 🛠️ Tech stack:

- Vue 3
- TypeScript
- FastAPI
- Vitest, Playwright, and Pytest

## 👨‍💻 Methodology:

Scrum, 2-week sprints

## 🗄️ Database Configuration

### PostgreSQL Environment Variables

Set PostgreSQL credentials in `backend/app/core/.env`, format:

```ini
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_SERVER=
POSTGRES_PORT=
POSTGRES_DB=
```

---

## 🐳 Running the project with Docker

### 1. Prerequisites

- Install Docker Desktop before proceeding: [Docker Desktop](https://www.docker.com/products/docker-desktop)

### 2. Clone the repository:

```bash
git clone https://github.com/KubaBrambor/FujiTech-students_app.git
cd FujiTech-students_app
```

### 3. Running the entire project with Docker

To build and run both frontend and backend services, use:

```bash
docker compose up --build
```

If you want to force a clean rebuild without cache, use:

```bash
docker compose build --no-cache
docker compose up
```

To stop the containers, run:

```bash
docker compose down
```

To remove images and volumes after stopping, run:

```bash
docker compose down --rmi all --volumes
```

### Running a single service with Docker

#### Running only the backend:

```bash
docker compose up --build backend
```

To restart only the backend container:

```bash
docker compose restart backend
```

#### Running only the frontend:

```bash
docker compose up --build frontend
```

To restart only the frontend container:

```bash
docker compose restart frontend
```

---

## ⚙️ Running the project natively (without Docker)

### 1. Clone the repository:

```bash
git clone https://github.com/KubaBrambor/FujiTech-students_app.git
cd FujiTech-students_app
```

### 2. Install dependencies:

#### Install backend dependencies and activate the virtual environment:

For pip users:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate   # On Windows: backend\.venv\Scripts\activate
pip install backend/
```

For uv users:

```bash
uv sync --project backend
```

#### Install frontend dependencies (using pnpm):

```bash
pnpm --dir frontend install
```

### 3. Run the services:

#### Run backend:

**You can run the backend using FastAPI:**

- for pip users

```bash
fastapi dev backend/main.py
```

- for uv users

```bash
uv run --project backend fastapi dev backend/main.py
```

**Or directly with Uvicorn:**

- for pip users

```bash
uvicorn backend.main:app --reload
```

- for uv users

```bash
uv run --project backend uvicorn backend.main:app --reload
```

#### Run frontend:

```bash
pnpm --dir frontend dev
```

---

## 📡 API Communication

The frontend communicates directly with the backend using a custom composable that wraps Nuxt’s `useFetch()`. This composable handles API requests without relying on a proxy, sending requests directly to the backend endpoints.

**Important:** The backend must be running before starting the frontend to ensure proper API communication.

---

## Useful Docker Commands

List running containers:

```bash
docker ps
```

Check container logs (replace `container_name` with the actual name):

```bash
docker logs -f container_name
```

Access a running container:

```bash
docker exec -it container_name sh
```

Prune unused images, containers, and networks:

```bash
docker system prune -a
```

---

## Additional Notes on Docker Build and Volumes

During the Docker image build process, your Dockerfile copies your source code and installs dependencies. This creates a "snapshot" of your application, including a properly installed `node_modules` folder (for frontend) and backend dependencies.

In a development environment, `docker-compose` mounts your local source code (e.g., `./frontend`) into the container. This allows for live updates (hot reload) when you change your code. However, mounting the entire folder from your host overwrites the content of the container – including the `node_modules` folder – if it exists on the host.

To prevent this, an anonymous volume is mounted for the `node_modules` folder (e.g., `- /app/frontend/node_modules`). This ensures that the dependencies installed during the image build are preserved, while the rest of your code remains synced with your host.

The `.dockerignore` file is used during the image build process to exclude unnecessary files (like your local `node_modules`) from being copied into the image. However, it does not affect what is mounted later as a volume by `docker-compose`.

---

This README provides instructions for running the project both in a Dockerized environment and natively, along with useful Docker commands and explanations of how build caching and volumes work.

Happy coding!

```

```
