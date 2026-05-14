# Development Roadmap

## Step 1: Project Setup

1. Initialize frontend dependencies for Next.js 15, Tailwind, shadcn/ui, Recharts, and React Query.
2. Initialize backend dependencies for FastAPI, SQLAlchemy, PostgreSQL, and OpenAI.
3. Add `.env` files from examples.
4. Configure local PostgreSQL and create the application database.

## Step 2: Backend Foundation

1. Add SQLAlchemy models and Alembic migrations.
2. Implement app configuration and database session management.
3. Create health, recommendation, comparables, feedback, and dashboard endpoints.
4. Add service-layer pricing logic.

## Step 3: Frontend Foundation

1. Build app shell with sidebar and top summary area.
2. Add route structure for login, dashboard, property details, recommendations, and analytics.
3. Introduce reusable cards, chart containers, and data display components.
4. Add typed API service layer.

## Step 4: First Vertical Slice

1. Property details form
2. Recommendation API integration
3. Recommendation summary card
4. Comparable cards
5. Feedback chat panel

## MVP Acceptance Criteria

- Analyst can input a property and receive a recommendation.
- Analyst can inspect ranked comparables.
- Analyst can provide feedback and trigger recalculation.
- Dashboard shows summary insights from stored recommendations.
