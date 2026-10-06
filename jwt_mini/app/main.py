from fastapi import FastAPI

from app.utils.jwt import create_access_token
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.utils.jwt import create_access_token
from app.routers import tasks, admin, auth, users


app = FastAPI(
    title="JWT Authentication",
    description="A FastApi project for Learning JWT Authent",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks.router)
app.include_router(admin.router)

@app.get("/")
def home():
    return{
        "message": "JWT task management API is running."
    }

@app.get("/test-token")
def test_token():
    token = create_access_token({
        "sub" : "testuser"
    })

    return {
        "access_token": token
    }