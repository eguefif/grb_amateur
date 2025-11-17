FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY main.py .

# Install dependencies (if any)
RUN uv sync

# Run the application
CMD ["uv", "run", "main.py"]
