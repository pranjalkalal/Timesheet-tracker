.PHONY: help install install-dev test lint format run run-docker stop clean

help:
	@echo "Timesheet Tracker - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  install          - Install production dependencies"
	@echo "  install-dev      - Install development dependencies"
	@echo "  test             - Run tests"
	@echo "  test-cov         - Run tests with coverage"
	@echo "  lint             - Run linting checks"
	@echo "  format           - Format code with ruff"
	@echo "  run              - Run development server locally"
	@echo "  run-docker       - Run with Docker Compose"
	@echo "  run-docker-dev   - Run development docker with auto-reload"
	@echo "  stop             - Stop Docker containers"
	@echo "  clean            - Clean up generated files"

install:
	cd backend && pip install -r requirements.txt

install-dev:
	cd backend && pip install -r requirements.txt && pip install pytest pytest-asyncio httpx ruff

test:
	cd backend && JWT_SECRET=test-secret pytest tests/ -v

test-cov:
	cd backend && JWT_SECRET=test-secret pytest tests/ -v --cov=app --cov-report=html

lint:
	cd backend && ruff check app tests

format:
	cd backend && ruff format app tests

run:
	cd backend && JWT_SECRET=my-secret-key uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-docker:
	JWT_SECRET=my-secret-key docker-compose up app

run-docker-dev:
	JWT_SECRET=dev-secret docker-compose up --profile dev app-dev

stop:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
	rm -f backend/app.db
