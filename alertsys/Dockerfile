FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV GCN_CLUSTER=test.gcn.nasa.gov
ENV BACKEND_URL="http://backend:8000/"
ENV TEST_CLIENT=False
ENV PROD=True

ADD . /app

WORKDIR /app
RUN uv sync --locked

CMD ["uv", "run", "main.py"]
