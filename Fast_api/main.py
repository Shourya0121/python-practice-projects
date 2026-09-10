from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

#BASEMODEL 
class Todo(BaseModel):
    id: int
    title: str
    content: str
    completed: bool = False

#PYDANTIC MODELS
class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Users full name"
        )
    age: int = Field(
        ge=18,
        le=100,
        description="Age must be between 18 and 100"
        )
    email: EmailStr

    bio: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional short bio"
    )

#RESPONSE MODEL
class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    bio: Optional[str] = None
    is_active: bool

#MEMORY DATABASE 
todos = [
    Todo(
         id=1,
        title="Learn FastApi",
        content="Practice fastapi CRUD oprations",
        completed=False
    ),
    Todo(
        id=2,
        title="Learn SqlAlchemy",
        content="BUild Database Modules",
        completed=False
    )
]
# GET ALL TODOS
@app.get("/todos")
def get_todos():
    return todos

# GET AN SINGLE TODOS BY ID
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found")

#TODOS POSTS
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return{
        "message": "Todo created successfully",
        "todo": todo    
    }

#UPDATE POST ROUTE
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):

    for index, todo in enumerate(todos):

        if todo.id == todo_id:
            todos[index] = updated_todo

            return {
                "message": "Todo updated successfully",
                "todo": updated_todo
            }

    raise HTTPException(
        status_code= 404,
        detail="Todo not found"
    )

#DELETE POST ROUTE
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            deleted_todo = todos.pop(index)

            return {
                "message": "Todo deleted successfully",
                "todo": deleted_todo
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.get("/")
def hello():
    return {"message": "Hello World!"}

#GET ROUTE WITH PATH PARAMETER 
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "message": "user found"
    }

#GET ROUTE WITH QUERY PARAMETER
@app.get("/search")
def search_users(name: str):
    return {
       "searching_for": name,   
        }

#GET ROUTE WITH PATH + QUERY PARAMETER
@app.get("/products/{product_id}")
def get_product(product_id: int, details: bool = False):
    return {
        "product_id": product_id,
        "show_details": details
    }

#POST ROUTE
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return {
        "id": 1,
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "bio": user.bio,
        "is_active": True
    }