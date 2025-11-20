# Gamma Ray Burst for Amateur Astronomers

A platform connecting amateur astronomers with the Fermi Satellite for Gamma Ray Burst (GRB) event notifications. This system enables astronomers to register for email notifications when the Fermi Satellite detects a GRB event, publish observations, and receive notifications.

## Features

- **Real-time GRB Alerts**: Track Fermi satellite alerts from NASA's GCN (General Coordinates Network) Kafka server
- **Email Notifications**: Register to receive GRB event notifications via email
- **Observation Publishing**: Share your astronomical observations with the community

## Roadmap

### Web
- [ ] Frontend + backend: add a system to register coordinate with email and precalculate observation angle
- [ ] Frontend: refine form and try to understand data
- [ ] Frontend: add a way to search observations
- [ ] Frontend: main page
	- [ ] add 5 last event cards
	- [ ] add 5 last observations
	- [ ] add the possibility to select and event and see observations
- [ ] check setup and how to works

### Production
- [ ] open a free account with AWS or cloudflare
- [ ] find a way to avoid bot
- [ ] add an https domain
- [ ] find a solution to easily push

### AlertSys

- [ ] add a system for notification: texto or email

### Security
- [ ] Add protection for end point to post new event
- [ ] Check all endpoint policy

## Architecture

The project consists of three main components:

### AlertSys (`alertsys/`)
The alert monitoring system that connects to NASA's GCN Kafka server to track Fermi satellite alerts.

### Web Backend (`web_backend/`)
FastAPI-based REST API server for registration or posting observation

### Frontend (`grb_front/`)
Vue 3 + TypeScript + Vite web application.

## Prerequisites

- Python 3.13+
- Node.js 20.19.0+ or 22.12.0+
- Docker and Docker Compose
- `uv` package manager
- GCN credentials (for production mode)

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd grb_for_amator
```

### 2. Start the Database

```bash
docker-compose up
```

This starts PostgreSQL 16 on port 5432 with the database `grb_db`.

### 3. Run other service

See the other README to run the frontend, AlertSys, backend.


The frontend will be available at `http://localhost:5173` (or the port shown in the terminal).

## Contact

[eguefif@gmail.com]
