Tendy (Monorepo)
=================

Overview
--------
This repository combines the Tendy backend (Python / FastAPI), the Flutter frontend, and supporting infra for local development and deployment.

Top-level layout
-----------------
- `backend/` — Python app (moved from previous `app/`), tests, backend Dockerfile and pyproject
- `frontend/` — Flutter app (copied from your local `myapp`) 
- `infra/` — docker-compose and infra helpers (place for nginx, reverse proxy etc.)
- `paper/` — LaTeX and analysis artifacts
- `scripts/` — useful developer scripts

Quick start (dev)
-----------------
1. Install prerequisites: Docker, Docker Compose, Flutter SDK (for mobile/web dev).
2. From repo root, run `make setup` (if present) or follow component instructions:
   - Backend: `cd backend && python -m pip install -r requirements.txt && uvicorn backend.app:app --reload`
   - Frontend (web): `cd frontend/myapp && flutter pub get && flutter run -d web-server`
3. To run combined services (if `infra/docker-compose.yml` added): `docker-compose -f infra/docker-compose.yml up --build`

Notes
-----
- The Flutter project was copied into `frontend/myapp`; the embedded Git metadata was removed and the project is now tracked in this repo.
- Python build files were moved under `backend/`.

If you want I can:
- Add a Makefile and dev scripts for standard tasks
- Create `infra/docker-compose.yml` that runs both services for local dev
- Add CI workflows for backend and frontend tests

Tell me which of the above you want me to add next and I will implement it.
