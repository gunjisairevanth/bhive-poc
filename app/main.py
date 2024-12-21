from fastapi import FastAPI, HTTPException
from app.models import UserCreate
from app.database import database
from pydantic import BaseModel
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

# Initialize FastAPI app
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to handle MongoDB insertion
async def insert_user(user: UserCreate):
    user_dict = jsonable_encoder(user)
    result = await database.get_collection("users").insert_one(user_dict)  # Insert user into MongoDB
    inserted_user = await database.get_collection("users").find_one({"_id": result.inserted_id})  # Fetch inserted user
    return inserted_user

# Create a registration endpoint
@app.post("/register", response_model=UserCreate)
async def register(user_create: UserCreate):
    db_user = await database.get_collection("users").find_one({"email": user_create.email})
    if db_user:
        raise HTTPException(status_code=401, detail="User Alredy Registered")
    user_create.password = hash_password(user_create.password)
    user = await insert_user(user_create)  # Insert user into the database
    if not user:
        raise HTTPException(status_code=400, detail="User registration failed")
    raise HTTPException(status_code=200, detail="User registration Sucessfully") 
