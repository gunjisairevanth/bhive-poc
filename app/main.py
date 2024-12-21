from fastapi import FastAPI, HTTPException
from app.models import UserCreate
from app.database import database
from pydantic import BaseModel
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()

# Helper function to handle MongoDB insertion
async def insert_user(user: UserCreate):
    user_dict = jsonable_encoder(user)  # Convert the Pydantic model to a dictionary
    result = await database.get_collection("users").insert_one(user_dict)  # Insert user into MongoDB
    inserted_user = await database.get_collection("users").find_one({"_id": result.inserted_id})  # Fetch inserted user
    return inserted_user

# Create a registration endpoint
@app.post("/register", response_model=UserCreate)
async def register(user_create: UserCreate):
    user = await insert_user(user_create)  # Insert user into the database
    if not user:
        raise HTTPException(status_code=400, detail="User registration failed")
    return user_create
