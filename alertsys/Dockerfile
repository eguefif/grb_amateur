FROM ghcr.io/astral-sh/uv:python3.14-alpine

ADD . /app

WORKDIR /app
RUN uv sync --locked

CMD ["uv", "run", "main.py"]
