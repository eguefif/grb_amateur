# Web Backend - GRB for Amateur

FastAPI-based web server for the Gamma Ray Burst notification platform.

## Overview

This backend service provides:
- User registration for GRB email notifications
- Client download endpoints
- Add observations

**Status**: Early development stage

## Dependencies

[python](https://www.python.org/downloads/)
[uv](https://docs.astral.sh/uv/#installation)
[just](https://just.systems/man/en/)

## Setup

Install dependencies using `uv`:

```bash
just setup
```

## Running

Start the development server:

```bash
uv run fastapi dev
```

## Database

The backend requires PostgreSQL. Start it via Docker from the project root:

```bash
cd ..
docker-compose up -d
```

## Project Structure

See the main [project README](../README.md) for complete architecture and setup instructions.
