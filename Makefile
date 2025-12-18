# Makefile for common tasks
.PHONY: setup dev up down backend-test frontend-test test build-front build-back lint

setup:
	python -m pip install -U pip
	python -m pip install -r backend/requirements-ci.txt
	@echo "Run 'make dev' to start services or run components individually."

dev:
	docker-compose -f infra/docker-compose.yml up --build

up:
	docker-compose -f infra/docker-compose.yml up -d --build

down:
	docker-compose -f infra/docker-compose.yml down

backend-test:
	cd backend && pytest -q

frontend-test:
	cd frontend/myapp && flutter pub get && flutter test

test: backend-test frontend-test

build-front:
	cd frontend/myapp && flutter pub get && flutter build web

build-back:
	docker build -t tendy-backend ./backend

lint:
	cd backend && ruff . || true
