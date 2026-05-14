# LeaseLens

LeaseLens is an AI-powered rental pricing tool prototype for real estate analysts. This repository is organized as a monorepo with a `frontend` Next.js application and a `backend` FastAPI service.

## Workspace Layout

```text
LeaseLens/
├─ docs/
├─ frontend/
└─ backend/
```

## What Exists Now

- Architecture and implementation planning docs
- Frontend scaffold for a SaaS-style analyst dashboard
- Persistent backend structure with async SQLAlchemy repositories and services
- PostgreSQL/SQLAlchemy schema definitions and Alembic migration scaffold
- Analysis history pages and recommendation timeline workflow
- Dockerized local PostgreSQL setup and demo seed script

## Setup Order

1. Read [docs/architecture.md](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/docs/architecture.md:1)
2. Read [docs/development-roadmap.md](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/docs/development-roadmap.md:1)
3. Configure [frontend/.env.example](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/.env.example:1) and [backend/.env.example](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/.env.example:1)
4. Start PostgreSQL with [docker-compose.yml](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/docker-compose.yml:1)
5. Run Alembic using [backend/alembic.ini](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/alembic.ini:1)
6. Seed demo data with [backend/scripts/seed_demo_data.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/scripts/seed_demo_data.py:1)
7. Start frontend and backend apps
8. Add a Gemini API key in `backend/.env` if you want AI-authored explanations and feedback interpretation

## Next Suggested Implementation Step

Runtime validation and hardening:

1. Install dependencies and run both apps
2. Execute migrations against local Postgres
3. Verify analysis create/recalculate/history flows end-to-end
4. Verify Gemini-backed explanation and feedback flows
5. Add auth and real user ownership
