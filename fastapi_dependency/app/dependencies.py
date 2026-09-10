import logging
from fastapi import Query

def pagination(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10,  ge=10, le=100)
):
    return {
        "skip": skip,
        "limit": limit
    }

#LOGGER FOR TODOS

def get_logger():
    return logging.getLogger("todo_api")

#DB sessions

def get_db():
    db = "Fake db sessions"

    try:
        yield db

    finally:
        print("DataBase cession closed")