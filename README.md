# Tendy - Multi‑Modal Attendance System

Tendy is a research prototype that explores and compares three attendance verification approaches: dynamic QR codes (active), Bluetooth proximity (passive), and a biometric liveness audit (social). This repository contains the **backend** (Python / FastAPI), the **frontend** (Flutter mobile + web), development **infrastructure**, and the project **paper** and analysis artifacts.

---

## Quick highlights

- Backend: FastAPI server for session management, TOTP QR generation, BLE presence, and check-in endpoints.
- Frontend: Flutter app demonstrating QR, BLE, and selfie flows (mobile + web).
- Research artifacts: LaTeX paper and analysis notebooks under `paper/`.
- Dev infra: `docker-compose` for local development and GitHub Actions CI included.

---

## Repository layout

- `backend/` - Python service, tests, Dockerfile, packaging
- `frontend/` - Flutter app source, tests, and web build output
- `infra/` - `docker-compose` and supporting infra (local dev)
- `paper/` - LaTeX source, figures, and notebooks
- `scripts/` - helper scripts and automation tasks

---

## Quick start (Development)

Prerequisites: Docker & Docker Compose. For Flutter development, install the Flutter SDK.

1. Clone the repo and install dev tooling (optional):

   ```bash
   make setup
   ```

2. Start both services locally (development mode):

   ```bash
   make dev
   ```

   - Backend will be available at: `http://localhost:8000`
   - Flutter web dev server (if used) runs at: `http://localhost:5000`

3. Run tests:

   ```bash
   make backend-test    # run backend pytest
   make frontend-test   # run flutter tests
   ```

---

## Running & debugging tips

- Backend: use `uvicorn backend.app:app --reload --port 8000` (or rely on `make dev`).
- Frontend: update `frontend/myapp/lib/config.dart` `AppConfig.apiBaseUrl` to point to your backend (use `10.0.2.2` for Android emulator, `127.0.0.1` for iOS simulator, or your host LAN IP for real devices).
- For CI debugging, check `.github/workflows/python-tests.yml` and `flutter.yml`.

---

## Contributing

We welcome issues and pull requests:

- Run `flutter analyze` and `dart format .` before opening PRs for the frontend.
- Run `pytest` for backend tests and keep coverage where possible.
- Add **clear doc comments** for public APIs and widgets.

---

## Contact

Author: **Michael Pisman** - mpisman@ucmerced.edu

---

*Status:* active research prototype - expect changes and refinements as experiments progress.
