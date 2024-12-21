from fastapi import FastAPI, HTTPException, APIRouter, Request, Response
from app.models import UserCreate, UserLogin, Token
from app.database import database
from pydantic import BaseModel
from bson import ObjectId
import requests
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from app.security import create_access_token
import uuid
from contextlib import asynccontextmanager
from app.utils import startup_tasks, shutdown_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_tasks()
    yield
    # Shutdown logic
    await shutdown_tasks()

app = FastAPI(lifespan=lifespan)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
prefix_router = APIRouter(prefix="/api/v1")


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

@prefix_router.post("/register", response_model=UserCreate)
async def register(user_create: UserCreate):
    db_user = await database.get_collection("users").find_one({"email": user_create.email})
    if db_user:
        raise HTTPException(status_code=401, detail="User Alredy Registered")
    user_create.password = hash_password(user_create.password)
    user = await insert_user(user_create)
    if not user:
        raise HTTPException(status_code=400, detail="User registration failed")
    raise HTTPException(status_code=200, detail="User registration Sucessfully") 


@prefix_router.post("/login", response_model=Token)
async def login(user: UserLogin, response: Response):
    db_user = await database.get_collection("users").find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user['user_id']})
    await database.get_collection("token").insert_one({
        "email" : db_user['user_id'],
        "token" : access_token
    })
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")
    return {"access_token": access_token, "token_type": "bearer"}


@prefix_router.get("/sync")
async def sync_funds_latest_details():
    url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest?Scheme_Type=Open"
    headers = {
        'x-rapidapi-key': "3732dec9a0msh7ee1adb6a3261d2p1be5c3jsnf7aebf6cd9ee",
        'x-rapidapi-host': "latest-mutual-fund-nav.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, list):
            for fund in response_data:
                scheme_code = fund.get("Scheme_Code")
                if scheme_code:
                    database.get_collection("fund_details").update_one(
                        {"Scheme_Code": scheme_code},
                        {"$set": fund},
                        upsert=True 
                    )
        else:
            scheme_code = response_data.get("Scheme_Code")
            if scheme_code:
                database.get_collection("fund_details").update_one(
                    {"Scheme_Code": scheme_code},
                    {"$set": response_data},
                    upsert=True
                )

        return {"message": "Data saved to MongoDB successfully!"}
    else:
        return {"message": f"Failed to fetch data"}


@prefix_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")  # This will remove the cookie
    return {"message": "Logout successful"}



app.include_router(prefix_router)