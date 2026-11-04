# Secure Task Management API

A backend learning project built with FastAPI, JWT authentication,
SQLAlchemy, Alembic, MySQL, and Docker.

## Run locally

Install dependencies and start the API:

```bash
pip install -r requirements.txt
python -m app.main
```

The API listens at <http://127.0.0.1:8001>. Interactive API docs are at
<http://127.0.0.1:8001/docs>.

## Planned features

- User registration and login
- Secure password hashing
- JWT-protected endpoints
- User-specific task CRUD
- MySQL database
- Alembic database migrations
- Docker Compose
- Automated tests

## Development status

Project setup and the initial FastAPI application are in place.