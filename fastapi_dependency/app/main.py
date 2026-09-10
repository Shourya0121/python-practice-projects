from fastapi import FastAPI

from app.routes.todos import router as todo_router



app = FastAPI(
    title="API PROJECT WITH DEPENDENCIES"
)

@app.get("/")
def home():
   return {
    "message": "todo project contains dependencies"
}

app.include_router(todo_router)