FROM ghcr.io/astral-sh/uv:python3.14-alpine

ADD . /app

WORKDIR /app
RUN uv sync --locked

CMD ["sh", "-c", "uv run alembic upgrade head && uv run fastapi run"]
