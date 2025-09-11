# Use official uv image that already includes Python + uv
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set working directory inside container
WORKDIR /app/backend

# Copy only project manifests first (helps with layer caching)
COPY pyproject.toml uv.lock* ./

# Where the virtualenv will live (persisted via the named volume)
ENV VENV_PATH=/app/backend/.venv
# Make sure venv's bin is first on PATH (even before it exists)
ENV PATH="${VENV_PATH}/bin:${PATH}"

# Copy the rest of the backend code
COPY . .

# Expose backend port
EXPOSE 8000

# On first run: if .venv is missing (fresh volume), install exactly what's in uv.lock;
# then start the app using the venv via `uv run`.
CMD ["/bin/sh", "-lc", "test -x \"$VENV_PATH/bin/python\" || uv sync --frozen; uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
