SecureWatch — API & Service Monitoring System

A backend service monitoring platform that automatically tracks the uptime and response time of registered services and APIs, alerting owners when something goes down.

Features
JWT Authentication — secure login with refresh token rotation and blacklisting
Automated Monitoring — Celery + Redis powered background task engine pings registered services on a schedule, measuring latency and detecting downtime
REST API — full CRUD for services and check history via Django REST Framework, with ownership-scoped access control
Email Alerts — automatic notification when a monitored service goes down
Security Hardening — API rate limiting/throttling, SSRF protection on registered URLs, strong password validation
Fully Containerized — Docker Compose orchestrates the entire stack (web, Celery worker, Celery beat, Redis, PostgreSQL) for consistent local development and deployment
Tech Stack

Backend: Python, Django, Django REST Framework Database: PostgreSQL Task Queue: Celery, Redis Auth: JWT (djangorestframework-simplejwt) Infrastructure: Docker, Docker Compose, Gunicorn, Render

Architecture Overview
User → REST API (JWT auth) → Django/DRF
                                  │
                                  ├── PostgreSQL (services, users, check history)
                                  │
                                  └── Celery Beat (scheduler, every 5 min)
                                          │
                                          ▼
                                  Celery Worker(s) → HTTP ping each service
                                          │
                                          ├── Write CheckResult to PostgreSQL
                                          └── Send email alert if down
Getting Started (Local Development with Docker)
Prerequisites
Docker Desktop installed and running
Git
Setup
Clone the repository
bash
   git clone https://github.com/PoonamBanga/SecureWatch-Service-Monitoring-System.git
   cd SecureWatch-Service-Monitoring-System
Create a .env file in the project root:
   DB_NAME=securewatch
   DB_USER=postgres
   DB_PASSWORD=your_chosen_password
   DB_HOST=db
   DB_PORT=5432
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   SECRET_KEY=your_django_secret_key
   DEBUG=True
Build and start the full stack:
bash
   docker-compose up --build
In a separate terminal, run migrations and create a superuser:
bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
Visit http://localhost:8000/admin/ and log in.
API Endpoints
Endpoint	Method	Description
/api/token/	POST	Obtain JWT access + refresh token
/api/token/refresh/	POST	Refresh an access token
/api/services/	GET, POST	List or create monitored services
/api/services/<id>/	GET, PUT, PATCH, DELETE	Manage a specific service
/api/check-results/	GET	List check history
/api/check-results/<id>/	GET	View a specific check result

All endpoints (except token issuance) require a valid JWT via the Authorization: Bearer <token> header. Data is scoped to the authenticated user's own services.

Project Status

Actively in development. Core monitoring pipeline, REST API, authentication, and security hardening are complete and tested. Deployment to Render is in progress.

Author

Poonam 