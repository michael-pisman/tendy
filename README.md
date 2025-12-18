Tendy
=====

Overview
--------
Tendy is a research prototype for a multi-modal attendance system that compares three verification approaches: dynamic QR codes (active), Bluetooth proximity (passive), and a biometric liveness audit (social). This repository contains the backend server (Python / FastAPI), a Flutter client (mobile + web), infrastructure for local development, and the project paper and analysis.

Key features
------------
- Backend: FastAPI server handling sessions, TOTP QR generation, BLE-assisted presence, and an audit endpoint for biometric images.
- Frontend: Flutter app implementing the three check-in flows (QR, BLE, Biometric) and demo UI.
- Research artifacts: analysis notebook and LaTeX paper in `paper/`.

Repository layout
-----------------
- `backend/` — Python service, tests, Dockerfile, packaging
- `frontend/` — Flutter project (app source, tests, web build output)
- `infra/` — docker-compose and supporting infra
- `paper/` — LaTeX source and analysis notebooks
- `scripts/` — helper scripts (dev tasks, builders)

Quick start (development)
-------------------------
Prerequisites: Docker, Docker Compose. For Flutter development, install Flutter SDK.

1. Install Python CI deps (optional):
   make setup
2. Run both services locally (dev):
   make dev
   - The backend will run on http://localhost:8000
   - The Flutter web dev server will run on http://localhost:5000
3. Run tests:
   make backend-test
   make frontend-test

Notes
-----
- The repo is organized as a monorepo for easier coordination between backend and frontend.
- CI workflows run backend Python tests and Flutter tests/build on push and pull requests.

Contributing
------------
Open issues or pull requests for bugs, feature requests, or documentation improvements. If you'd like, I can add more CI checks, deployment scripts, or packaging workflows.

Contact
-------
Author: Michael Pisman — mpisman@ucmerced.edu
