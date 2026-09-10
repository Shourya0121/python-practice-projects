from fastapi import HTTPException, Depends, APIRouter

from app.modal import Todo
from app.dependencies import pagination, get_db, get_logger

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

todos = [

    Todo(
        id=1,
        title= "Learning Python",
        content= "Learn FastApi",
        completed= False

    ),
    Todo(
        id= 2,
        title= "Practice Python",
        content= "practice FastApi",
        completed= False
    
    ),
    Todo(
        id= 3,
            title= "Build Project",
            content= "create FastApi project structure",
            completed= False
        
            )
]

@router.get("/")
def get_todos(
    pagination_params: dict = Depends(pagination),
    logger = Depends(get_logger),
    db = Depends(get_db)
):
    logger.info("Geeting all Todos")

    skip = pagination_params["skip"]
    limit = pagination_params["limit"]

    return{
        "skip": skip,
        "limit": limit,
        "todos":todos[skip: skip + limit]
    }

#CRUD 
@router.get("/{todo_id}")
def get_todo(
    todo_id: int,
    logger = Depends(get_logger),
    db=Depends(get_db)       
):

    logger.info(f"Getting todo by id{todo_id}")

    for todo in todos:
        if todo.id == todo_id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )

@router.post("/")
def create_todo(
    todo: Todo,
    logger = Depends(get_logger),
    db = Depends(get_db)
):

    logger.info(f"creating todo by id{todo.id}")

    todos.append(todo)

    return{
            "massage": "todo was created successfuly",
            "todo": todo
    }

    #update todo

@router.put("/{todo_id}")
def updated_todo(
        todo_id: int,
        updated_todo: Todo,
        logger= Depends(get_logger),
        db = Depends(get_db)
    ):
        logger.info(f"udating todo by todo id{todo_id}")

        for index, todo in enumerate(todos):
            if todo.id == todo_id:
                todos[index] = updated_todo

                return {
                    "message": "successfully updated todo",
                    "todo": updated_todo
                }

        raise HTTPException(
            status_code=404,
            detail="todo not found"
        )


#DELETED todo

@router.delete("/{todo_id}")
def deleted_todo(
    todo_id: int,
    logger = Depends(get_logger),
    db = Depends(get_db)
):
    logger.info(f"deleting todo by todo id{todo_id}")

    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = todos.pop(index)

    return {
        "massage": "todo deleted successfully",
        "todo": deleted_todo
    }

            

