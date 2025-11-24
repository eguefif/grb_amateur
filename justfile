run-dev: 
    docker compose -f compose-core.yml up

run-prod:
    docker compose -f compose-core.yml -f compose-prod.yml up

front:
    cd web_frontend && npm run dev

back:
    cd web_backend && uv run fastapi dev

lint:
    cd web_backend && uv run ruff format && uv run ruff check --fix
    cd alertsys && uv run ruff format && uv run ruff check --fix
    cd web_frontend && npm run lint -- --fix
