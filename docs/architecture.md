# LeaseLens Architecture

## 1. Product Goal

LeaseLens simulates an enterprise-grade AI pricing assistant that helps real estate analysts estimate rental prices, inspect comparable properties, understand neighborhood signals, and iteratively refine recommendations through natural-language feedback.

## 2. High-Level Architecture

```text
Frontend (Next.js)
  ├─ Analyst dashboard UI
  ├─ Property intake workflows
  ├─ Recommendation and comparables views
  └─ Chat feedback experience

Backend (FastAPI)
  ├─ Recommendation orchestration
  ├─ Comparable ranking service
  ├─ Neighborhood scoring service
  ├─ Feedback interpretation service
  └─ OpenAI integration layer

Data Layer (PostgreSQL)
  ├─ Properties
  ├─ Comparable properties
  ├─ Recommendations
  ├─ Feedback events
  ├─ Neighborhood metrics
  └─ Users
```

## 3. Frontend Folder Structure

```text
frontend/
├─ app/
│  ├─ login/
│  ├─ dashboard/
│  ├─ properties/
│  ├─ recommendations/
│  └─ analytics/
├─ components/
├─ features/
├─ services/
├─ hooks/
├─ lib/
└─ types/
```

## 4. Backend Folder Structure

```text
backend/
├─ app/
│  ├─ api/
│  │  └─ routes/
│  ├─ ai/
│  ├─ core/
│  ├─ db/
│  ├─ models/
│  ├─ schemas/
│  └─ services/
├─ tests/
└─ alembic/
```

## 5. Database Schema

### `users`

- `id`
- `email`
- `full_name`
- `role`
- `created_at`

### `properties`

- `id`
- `user_id`
- `address`
- `city`
- `state`
- `zip_code`
- `property_type`
- `bedrooms`
- `bathrooms`
- `area_sqft`
- `year_built`
- `parking_spaces`
- `has_gym`
- `has_pool`
- `pet_friendly`
- `latitude`
- `longitude`
- `created_at`

### `neighborhood_metrics`

- `id`
- `property_id`
- `school_quality_score`
- `flood_risk_score`
- `transit_score`
- `road_noise_score`
- `neighborhood_appeal_score`
- `crime_index`
- `walkability_score`
- `updated_at`

### `comparable_properties`

- `id`
- `source_property_id`
- `address`
- `monthly_rent`
- `bedrooms`
- `bathrooms`
- `area_sqft`
- `distance_miles`
- `similarity_score`
- `match_percentage`
- `selection_reason`
- `metadata`
- `created_at`

### `pricing_recommendations`

- `id`
- `property_id`
- `recommended_rent`
- `rent_low`
- `rent_high`
- `confidence_score`
- `price_per_sqft`
- `reasoning_summary`
- `adjustment_factors`
- `created_by_ai`
- `created_at`

### `analyst_feedback`

- `id`
- `recommendation_id`
- `user_id`
- `feedback_text`
- `sentiment`
- `parsed_intent`
- `pricing_adjustment`
- `created_at`

## 6. API Design

### `POST /api/v1/pricing/recommendation`

Creates a recommendation from property details and neighborhood context.

### `POST /api/v1/pricing/comparables`

Ranks comparable properties for a target property.

### `POST /api/v1/pricing/feedback`

Processes natural-language analyst feedback, stores it, and recalculates pricing output.

### `GET /api/v1/dashboard/insights`

Returns KPI cards, chart data, and analyst activity summaries.

### `GET /api/v1/health`

Operational health check.

## 7. AI Workflow

1. Normalize property input.
2. Fetch neighborhood metrics and comparable inventory.
3. Run weighted pricing logic for baseline recommendation.
4. Optionally call OpenAI for narrative explanation and feedback interpretation.
5. Rank comparables using weighted similarity scoring or pgvector-assisted retrieval.
6. Accept analyst feedback and adjust pricing factors.
7. Persist recommendations and feedback events for future learning.

## 8. Pricing Logic

Recommended weighted baseline:

- Location: 25%
- Area size: 15%
- Amenities: 10%
- School quality: 10%
- Flood risk: 5%
- Nearby transit: 10%
- Road noise: 5%
- Neighborhood appeal: 10%
- Comparable rental history: 10%

## 9. Comparable Matching Logic

- Distance from subject property
- Similar unit size
- Bed and bath alignment
- Amenity similarity
- Neighborhood profile similarity
- Historical pricing proximity

## 10. UI Wireframe Suggestions

- Login page with a left-side positioning panel and right-side auth card
- Dashboard with KPI row, charts, and activity feed
- Property details page with form, map context, and sticky recommendation preview
- Recommendation page with price band, confidence, and explanation
- Comparables panel with sortable cards and inclusion controls
- Feedback chat with analyst and AI conversation layout
- Analytics page with volume, override, and confidence trends

## 11. Recommended Libraries

Frontend:

- `next`
- `tailwindcss`
- `class-variance-authority`
- `clsx`
- `tailwind-merge`
- `lucide-react`
- `recharts`
- `react-hook-form`
- `zod`
- `@tanstack/react-query`

Backend:

- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `psycopg[binary]`
- `alembic`
- `pydantic-settings`
- `openai`
- `pgvector`

## 12. Development Order

1. Set up monorepo scaffolding
2. Define database models and migrations
3. Build backend API contracts
4. Build frontend layout and routes
5. Implement property intake and recommendation flow
6. Add comparables ranking and UI interactions
7. Add feedback chat and recalculation
8. Add analytics dashboards
9. Harden validation, auth, and observability

## 13. Best Practices

- Keep pricing logic deterministic before layering LLM reasoning on top.
- Treat OpenAI output as assistive, not authoritative.
- Store both baseline and adjusted recommendation values.
- Version recommendation logic for auditability.
- Separate API schemas from ORM models.
