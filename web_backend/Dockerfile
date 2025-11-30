FROM ghcr.io/astral-sh/uv:python3.14-alpine

ENV DB_ECHO=False
ENV DOMAIN=http://www.grb-amateur.space
ENV DEV=False
ENV PROD=True

ADD . /app

WORKDIR /app
RUN uv sync --locked

CMD ["sh", "-c", "uv run alembic upgrade head && uv run fastapi run"]
