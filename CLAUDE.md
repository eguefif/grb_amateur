# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a platform connecting Amateur Astronomers with the Fermi Satellite for Gamma Ray Burst (GRB) event notifications. The system enables astronomers to register for email notifications when the Fermi Satellite detects a GRB event, publish observations, and receive notifications directly to client applications.

## Architecture

The project is organized into three main components:

### 1. AlertSys (`alertsys/`)
The alert monitoring system that connects to NASA's GCN (General Coordinates Network) Kafka server to track Fermi satellite alerts.

- **Main entry point**: `alertsys/main.py`
- **MessageClient abstraction** (`message_client.py`): Provides a switchable client between test mode (for development) and production mode (using gcn-kafka). The `test` parameter controls which mode is used.
- **Historical data script** (`historical.py`): Retrieves historical GRB events from the last 3 days using Kafka offset management
- **Kafka topics monitored**:
  - `gcn.classic.text.FERMI_GBM_ALERT`
  - `gcn.classic.text.FERMI_GBM_FIN_POS`
  - `gcn.classic.text.FERMI_GBM_GND_POS`
  - `gcn.classic.text.FERMI_GBM_POS_TEST`

### 2. Web Backend (`web_backend/`)
FastAPI-based web server (currently in early development stage).

- **Status**: Minimal skeleton implementation
- **Planned**: User registration, notification management, client download endpoints

### 3. Frontend (`grb_front/`)
Vue 3 + TypeScript + Vite application for the web interface.

- **Framework**: Vue 3 with Composition API
- **Build tool**: Vite
- **Language**: TypeScript with type checking via `vue-tsc`
- **Routing**: Vue Router

## Development Setup

### Prerequisites
- Python 3.13+
- Node.js 20.19.0+ or 22.12.0+
- Docker and Docker Compose (for PostgreSQL)
- `uv` package manager for Python projects

### Environment Variables
Required credentials in `.env` file (alertsys only):
```
GCN_CLIENT=<your-gcn-client-id>
GCN_KEY=<your-gcn-key>
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=grb_db
```

### Database
Start PostgreSQL via Docker:
```bash
docker-compose up -d
```

This starts PostgreSQL 16 on port 5432 with the database `grb_db`.

### AlertSys Development
```bash
cd alertsys
uv sync                    # Install dependencies
uv run main.py            # Run with test mode (no GCN credentials needed)
uv run historical.py      # Fetch historical events (requires GCN credentials)
```

### Web Backend Development
```bash
cd web_backend
uv sync
uv run main.py
```

### Frontend Development
```bash
cd grb_front
npm install               # Install dependencies
npm run dev              # Start dev server with hot reload
npm run build            # Type-check and build for production
npm run type-check       # Run TypeScript type checking
npm run lint             # Lint and auto-fix with ESLint
npm run format           # Format code with Prettier
```

## Key Technical Decisions

### Security Model
The project uses a public/private key system for client authentication instead of traditional email/password:
- All clients receive messages encoded with a private key
- Clients use a public key to decrypt messages
- This prevents attackers from diverting legitimate clients

### Test Mode Pattern
The `MessageClient` class in alertsys implements a test mode that allows development without GCN credentials. When `test=True`, it yields mock messages instead of connecting to the real Kafka server.

## Project Structure Notes

- **Python projects** use `uv` for dependency management with `pyproject.toml`
- **Frontend** follows standard Vue 3 + Vite structure with TypeScript
- **Database** is managed via Docker Compose for local development
- **No tests** currently exist in the codebase

## Roadmap Context

Current implementation status:
1. ✓ AlertSys can track Fermi alerts from NASA GCN Kafka server
2. ⚠️ Website for email registration (early stage)
3. ☐ Client download functionality
4. ☐ Client application development
