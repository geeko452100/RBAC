# Enterprise Role-Based Access Control (RBAC) API

A headless, production-ready authentication and authorization backend system. This project implements a secure, modular permissions architecture designed to handle hierarchical enterprise access rules.

Built entirely as a backend logic engine with **zero frontend visuals**.

## 🏗️ System Architecture & Data Flow

The system isolates API routing from business logic layers using a standard modular pattern:

```text
[Client Request] ──> [FastAPI Router] ──> [Auth / RBAC Service Layer]
                                                    │
                                                    ▼
[PostgreSQL DB]  <── [SQLAlchemy ORM]  <── [Data Validation (Pydantic)]
```

### Core Database Relationships
* **Users**: Linked to exactly one Role (`Many-to-One`). Account deletion is strictly restricted if a active link exists.
* **Roles**: Associated with multiple Permissions using a custom composite-key join table (`Many-to-Many`).
* **Permissions**: Standalone modular action cards (e.g., `read_records`, `write_prescriptions`) optimized with database indices for fast-lookup execution.

## 🛠️ Technology Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI (Asynchronous execution engine)
* **Database:** PostgreSQL (Relational integrity engine)
* **ORM:** SQLAlchemy (Modern 2.0 type-hinted architecture)
* **Infrastructure:** Docker Desktop (Database isolation container)

## 🚀 Getting Started (Local Development)

### 1. Prerequisite Infrastructure
Ensure **Docker Desktop** is installed and running. Spin up the isolated PostgreSQL instance with the following command:

```bash
docker run --name rbac-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=secret_password -e POSTGRES_DB=rbac_system -p 5432:5432 -d postgres:latest
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```ini
DATABASE_URL=postgresql+asyncpg://admin:secret_password@localhost:5432/rbac_system
```

### 3. Python Application Installation
Set up your isolated virtual environment and pull down project dependencies:

```bash
# Create and activate environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 4. Running the Application
Launch the FastAPI development server:
```bash
uvicorn app.main:app --reload
```
Once active, visit `http://127.0.0` to access the automatically generated interactive Swagger API documentation workspace.
