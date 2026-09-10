from fastapi import FastAPI
from Router.notes import router as notes_router

app = FastAPI(
    title="Notes API",
    description="A Simple CRUD project."
)

app.include_router(notes_router)

@app.get("/")
def root():
    return {
        "message": "welcome to notes API"
    }
