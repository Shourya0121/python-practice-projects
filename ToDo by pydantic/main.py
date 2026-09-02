from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

todos = []
next_id = 1

class Todo(BaseModel):
    title: str
    content: str
    completed: bool = False



@app.get("/")
def root():
    return{"message" :"Todo api is working!"}


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo ):
    global next_id

    new_todo = {
        "id": next_id,
        "title": todo.title,
        "content": todo.content,
        "completed": todo.completed

    }

    todos.append(new_todo)

    next_id += 1
    return new_todo

@app.get("/todos")
def get_todos():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos   :
        if todo["id"] == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found!"
    )

@app.delete("/todos{todo_id}")
def delete_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return{"message": "Todo Deleted Successfully"}

    raise HTTPException(
        status_code=404,
        detail="Todo not found!"
    )

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = updated_todo.title
            todo["content"] = updated_todo.content
            todo["completed"] = updated_todo.completed

            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found!"
    )


