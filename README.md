# Darukaa.Earth

Geospatial project management for carbon and biodiversity initiatives.

## Local setup

1. Copy `.env.example` to `.env` and supply a PostGIS-enabled PostgreSQL URL and a Mapbox token.
2. Run `cd backend; alembic upgrade head; python -m app.seed`.
3. Install the frontend packages with `cd frontend; npm ci`, then run `npm run dev`.

The API is served at `http://localhost:8000`; the Vite client defaults to port 5173. Set `COOKIE_SECURE=true` for HTTPS deployments.
