from pydantic import BaseModel

# Pydantic model for creating a user
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

    class Config:
        orm_mode = True
