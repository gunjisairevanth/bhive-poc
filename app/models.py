from pydantic import BaseModel, Field
import uuid
# Pydantic model for creating a user
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
        on_encoders = {
            uuid.UUID: lambda v: str(v)
        }

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str