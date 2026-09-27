# API Health & Latency Monitor

A lightweight, asynchronous REST API built with **Python**, **FastAPI**, and **httpx** designed to monitor the health, availability, and response latency of target URLs.

## Features
- **Async Execution:** Utilizes `httpx` and `asyncio` for non-blocking HTTP health checks across multiple endpoints.
- **Data Persistence:** Integrated SQLite database context managers to securely store HTTP status codes, uptime flags, and latency measurements.
- **Dockerized Environment:** Containerized using Docker for consistent local testing and seamless deployment.

## Tech Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI, Uvicorn
- **HTTP Client:** httpx
- **Database:** SQLite
- **DevOps:** Docker, Git

## Setup & Running Locally

### 1. Run with Docker
```bash
docker build -t api-monitor .
docker run -p 8000:8000 api-monitor