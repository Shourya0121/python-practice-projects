from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    completed: bool
    owner_id: int

    class Config:
        from_attributes=True


    class UserBase(BaseModel):
        username: str
        email: str

    class UserCreate(UserBase):
        pass

    class UserResponse(UserBase):
        id: int
        items: list[ItemResponse] = []

        class Config:
            from_attributes=True
