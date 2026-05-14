# LeaseLens Project Handbook

## Overview

LeaseLens is an AI-powered rental pricing platform prototype for real estate analysts. It is designed to simulate an enterprise-grade pricing assistant that can:

- collect detailed rental property inputs
- generate pricing recommendations
- explain pricing decisions
- rank comparable properties
- accept analyst feedback
- recalculate recommendations over time
- persist analysis history and recommendation revisions

The project is organized as a monorepo with:

- `frontend/`: Next.js 15, TypeScript, Tailwind CSS
- `backend/`: FastAPI, SQLAlchemy, PostgreSQL, Alembic

## Product Goals

The application is intended to feel like a modern AI analytics SaaS product for rental pricing teams. The target user is a real estate analyst who needs:

- a structured property intake workflow
- recommendation confidence and explanation
- transparent comparable selection
- feedback-driven recalculation
- persistent history and revision tracking

## Current Stack

### Frontend

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- Zustand
- Recharts
- React Hook Form
- Zod

### Backend

- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- Pydantic 1
- Google Gemini via `google-genai`
- Psycopg 3

## AI Provider

The project was originally scoped around OpenAI, but the codebase has now been switched to Gemini.

Current Gemini-related configuration:

- `GEMINI_API_KEY`
- `GEMINI_MODEL`

Current Gemini integration points:

- recommendation explanation generation
- feedback interpretation

Fallback behavior still exists:

- if Gemini is not configured
- if Gemini returns unusable output
- if JSON parsing fails

In those cases, deterministic pricing logic continues to work.

## High-Level Architecture

```text
Frontend
  -> analyst enters property data
  -> frontend posts to backend analysis API
  -> frontend renders recommendation, comparables, feedback history, timeline

Backend
  -> validates request
  -> runs pricing engine
  -> optionally enriches reasoning with Gemini
  -> persists analysis, recommendation, comparables, history, events, feedback
  -> returns full analysis detail

Database
  -> stores properties
  -> stores analyses
  -> stores recommendation versions
  -> stores comparables and comparable adjustments
  -> stores feedback messages and system events
```

## Core User Flows

### 1. New Analysis

User opens:

- `/dashboard/new-analysis`

User can:

- enter property details
- submit property analysis
- receive a recommendation
- inspect confidence and factor breakdown
- inspect comparable properties

### 2. Recommendation Refinement

User can:

- increase or decrease comparable weight
- remove comparables
- mark comparables irrelevant
- submit chat-style pricing feedback

The backend then:

- recalculates recommendation state
- persists a new recommendation version
- writes recommendation history
- logs events
- stores feedback

### 3. History and Reopen

User opens:

- `/dashboard/history`
- `/dashboard/history/[id]`

User can:

- see prior analyses
- inspect recommendation evolution
- reopen a saved analysis session

## Frontend Structure

```text
frontend/
├─ app/
│  ├─ dashboard/
│  │  ├─ history/
│  │  └─ new-analysis/
│  └─ login/
├─ components/
│  ├─ dashboard/
│  ├─ layout/
│  └─ ui/
├─ features/
│  └─ pricing-recommendation/
├─ hooks/
├─ services/
└─ types/
```

### Important Frontend Files

- [frontend/app/dashboard/new-analysis/page.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/app/dashboard/new-analysis/page.tsx:1)
- [frontend/app/dashboard/history/page.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/app/dashboard/history/page.tsx:1)
- [frontend/app/dashboard/history/[id]/page.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/app/dashboard/history/%5Bid%5D/page.tsx:1)
- [frontend/features/pricing-recommendation/analysis-form.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/features/pricing-recommendation/analysis-form.tsx:1)
- [frontend/features/pricing-recommendation/recommendation-results.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/features/pricing-recommendation/recommendation-results.tsx:1)
- [frontend/features/pricing-recommendation/comparable-panel.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/features/pricing-recommendation/comparable-panel.tsx:1)
- [frontend/features/pricing-recommendation/feedback-chat.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/features/pricing-recommendation/feedback-chat.tsx:1)
- [frontend/hooks/use-analysis-store.ts](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/hooks/use-analysis-store.ts:1)
- [frontend/services/analyses.ts](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/services/analyses.ts:1)

### Frontend State

The frontend uses Zustand to maintain:

- active analysis payload
- loaded persisted analysis
- loading and updating flags
- error state

The canonical state store is:

- [frontend/hooks/use-analysis-store.ts](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/hooks/use-analysis-store.ts:1)

### Frontend Pages

Currently implemented:

- `/`
- `/login`
- `/dashboard`
- `/dashboard/new-analysis`
- `/dashboard/history`
- `/dashboard/history/[id]`

## Backend Structure

```text
backend/
├─ app/
│  ├─ ai/
│  ├─ api/
│  │  └─ routes/
│  ├─ core/
│  ├─ db/
│  ├─ migrations/
│  ├─ models/
│  ├─ repositories/
│  ├─ schemas/
│  ├─ services/
│  │  └─ ai/
│  └─ utils/
├─ scripts/
├─ Dockerfile
├─ alembic.ini
└─ requirements.txt
```

### Important Backend Files

- [backend/app/main.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/main.py:1)
- [backend/app/core/config.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/core/config.py:1)
- [backend/app/db/session.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/db/session.py:1)
- [backend/app/api/routes/analyses.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/api/routes/analyses.py:1)
- [backend/app/api/routes/pricing.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/api/routes/pricing.py:1)
- [backend/app/services/analysis_service.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/services/analysis_service.py:1)
- [backend/app/services/pricing_engine.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/services/pricing_engine.py:1)
- [backend/app/services/ai/gemini_service.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/services/ai/gemini_service.py:1)
- [backend/app/repositories/analysis_repository.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/repositories/analysis_repository.py:1)
- [backend/app/migrations/versions/0001_initial_schema.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/migrations/versions/0001_initial_schema.py:1)

## Database Design

The backend is designed around persistent analyses and recommendation versioning.

### Main Tables

- `users`
- `properties`
- `property_analyses`
- `neighborhood_metrics`
- `pricing_recommendations`
- `comparable_properties`
- `comparable_adjustments`
- `analyst_feedback`
- `recommendation_history`
- `recommendation_events`

### Persistence Goals

The system is designed to persist:

- property intake details
- each analysis session
- each recommendation version
- feedback-driven recommendation changes
- comparable actions
- recommendation confidence changes
- recommendation event trail

## API Surface

### Main Analysis Endpoints

- `POST /api/v1/analyses`
- `GET /api/v1/analyses`
- `GET /api/v1/analyses/{id}`
- `POST /api/v1/analyses/{id}/feedback`
- `POST /api/v1/analyses/{id}/recalculate`
- `GET /api/v1/analyses/{id}/history`

### Other Endpoints

- `GET /api/v1/health`
- `GET /api/v1/dashboard/insights`

### Compatibility Pricing Endpoints

There is also a pricing route file:

- [backend/app/api/routes/pricing.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/api/routes/pricing.py:1)

This exists as a bridge during transition, but the main persistent workflow should use:

- `/api/v1/analyses`

## Recommendation Logic

The pricing engine is deterministic at its base and can be enhanced by Gemini for better explanations and feedback interpretation.

### Deterministic Logic Currently Covers

- property size influence
- amenities
- school quality
- flood risk
- transit score
- road noise
- neighborhood appeal
- simple market benchmark

### Comparable Logic Currently Covers

- mock comparable generation
- similarity score
- match percentage
- comparable action handling
- weight updates
- removal and irrelevance

### Feedback Logic

Current feedback logic supports:

- deterministic fallback rules
- Gemini-based feedback interpretation when configured

## Runtime Status

### Verified

- frontend dependencies installed
- frontend production build passes
- backend dependency installation now works locally on Python 3.14 after switching to a Pydantic 1-compatible setup
- backend syntax checks passed during development
- Gemini provider wiring exists in code

### Not Yet Fully Verified End-to-End

- local PostgreSQL migration execution
- local seed execution
- backend live boot against local database
- full browser-tested create/recalculate/history round trip
- Gemini live response flow with a real key

## Important Runtime Notes

### Shell Note

Some earlier instructions used PowerShell syntax. If using `cmd`, do not use:

```text
$env:PYTHONPATH="."
```

That is PowerShell-only.

The Alembic environment file was patched so manual `PYTHONPATH` setup should no longer be required.

### Python Note

The original backend dependency choices conflicted with Python 3.14 due to wheel/build issues. The backend was adjusted to run on the machine’s local Python runtime by:

- removing asyncpg
- using psycopg-based DB access
- switching to Pydantic 1

### Docker Note

Docker CLI is installed, but Docker Desktop daemon was not running and service startup was blocked on the host. Because of that, local runtime testing shifted toward the existing local PostgreSQL service.

## Environment Variables

### Backend

Expected `backend/.env` values:

```env
APP_NAME=LeaseLens API
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/leaselens
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
API_V1_PREFIX=/api/v1
```

### Frontend

Expected `frontend/.env.local` values:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
NEXT_PUBLIC_MAP_PROVIDER=mapbox
```

## Manual Setup Steps

### Backend

From `backend/`:

1. Install dependencies

```bat
python -m pip install -r requirements.txt
```

2. Run migrations

```bat
alembic upgrade head
```

3. Seed demo data

```bat
python scripts\seed_demo_data.py
```

4. Start backend

```bat
uvicorn app.main:app --reload
```

### Frontend

From `frontend/`:

1. Install dependencies

```bat
npm install
```

2. Start frontend

```bat
npm run dev
```

3. Production build verification

```bat
npm run build
```

## Seed Script

Demo seed script:

- [backend/scripts/seed_demo_data.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/scripts/seed_demo_data.py:1)

It creates:

- a demo property
- an initial analysis
- at least one recalculation flow

## Documentation Files Already Present

- [README.md](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/README.md:1)
- [docs/architecture.md](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/docs/architecture.md:1)
- [docs/development-roadmap.md](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/docs/development-roadmap.md:1)

This handbook is intended to be the single most complete project reference.

## Current UI Capabilities

The frontend already includes:

- modern dashboard shell
- sidebar navigation
- login screen
- analysis intake form
- price recommendation display
- confidence meter
- pricing factor visualization
- neighborhood radar visualization
- comparable cards with actions
- feedback chat panel
- analysis history page
- analysis detail timeline

## Current Limitations

### Backend

- auth is not implemented
- role-based access is not implemented
- recommendation engine is still partly synthetic
- comparables are still generated rather than sourced from real datasets
- Gemini output validation is lightweight and should be hardened further

### Frontend

- no authentication guard yet
- no toast system yet
- no command palette yet
- no dark mode yet
- no full loading skeleton design system yet

### Deployment

- Docker runtime path exists but was not fully verified on this host
- Vercel/Render/Railway deployment config is not finalized

## Recommended Next Steps

### Highest Priority

1. finish local migration and seed verification
2. boot backend successfully against real Postgres
3. test analysis creation and history persistence end-to-end
4. confirm Gemini explanation flow with a real key

### After Runtime Is Stable

1. add auth and protected routes
2. improve Gemini feedback schema validation
3. make comparable ranking more realistic
4. expand analytics dashboard
5. prepare deployment config

## Git Hygiene

The repo now includes a stronger `.gitignore` that covers:

- env files
- Python caches
- Next build output
- node modules
- logs
- local editor/system artifacts

Tracked lockfile:

- `frontend/package-lock.json`

This is intentionally not ignored.

## File Summary

If you need a minimal “where do I look first” list, start here:

- [README.md](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/README.md:1)
- [docs/project-handbook.md](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/docs/project-handbook.md:1)
- [backend/app/services/analysis_service.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/services/analysis_service.py:1)
- [backend/app/services/pricing_engine.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/services/pricing_engine.py:1)
- [backend/app/services/ai/gemini_service.py](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/backend/app/services/ai/gemini_service.py:1)
- [frontend/features/pricing-recommendation/analysis-workspace.tsx](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/features/pricing-recommendation/analysis-workspace.tsx:1)
- [frontend/hooks/use-analysis-store.ts](/C:/Users/Admin/OneDrive/Desktop/Projects/LeaseLens/frontend/hooks/use-analysis-store.ts:1)

## Final Note

This project is no longer just a loose scaffold. It now has:

- a defined architecture
- a persisted analysis domain
- history and revision tracking
- a working frontend build
- Gemini integration points
- a path to demo-ready runtime verification

The remaining work is primarily runtime stabilization, live API verification, stronger AI guardrails, authentication, and deployment polish.
