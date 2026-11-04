from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.tasks import router as tasks_router
app = FastAPI(
    title="Secure Task Management API",
    description="A learning project for FastAPI, JWT, MYSQL, Alembic and Docker.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Secure Task Management API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(tasks_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)

