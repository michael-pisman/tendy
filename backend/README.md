Backend (FastAPI)
==================

Overview
--------
This folder contains the FastAPI backend for Tendy. It exposes endpoints for session management and check-ins, and it stores logs in MongoDB using Beanie + Motor.

Quick start
-----------
1. Create and activate a Python environment (recommended Python 3.11+).
2. Install dev/test dependencies:

   python -m pip install -r requirements-cli.txt

   (Alternatively, use `backend/requirements-ci.txt` for CI/dev.)

3. Run locally (requires a running MongoDB instance):

   export MONGODB_URI=mongodb://localhost:27017
   uvicorn app.app:app --reload --port 8000

Tests
-----
Run unit tests from the repository root:

    make backend-test

Notes
-----
- The project uses Beanie for ODM models; during development, a fallback in-memory store is used when the DB is unavailable.
- For production use, configure a persistent MongoDB instance and set `MONGODB_URI` and `MONGODB_DBNAME`.
