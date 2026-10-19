from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db

app = FastAPI(title="MySQL Task Tracker API")


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email Already Registered")

    new_user = models.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/users/{user_id}/items", response_model=schemas.ItemResponse)
def create_item_for_user(
    user_id: int, item =  schemas.ItemCreate, db: Session = Depends(get_db)
):

   db_user = db.query(models.User).filter(models.User.id == user_id).first()
   if not db_user:
       raise HTTPException(status_code=404, detail="User not found")

   new_item = models.Item(**item.dict(), owner_id=user_id)
   db.add(new_item)
   db.commit()
   db.refresh(new_item)
   return new_item

@app.get("/users/{user_id}/items", response_model=list[schemas.ItemResponse])
def get_user_items(user_id: int, db: Session = Depends(get_db)):
    items = db.query(models.Item).filter(models.Item.owner_id == user_id).all()
    return items
