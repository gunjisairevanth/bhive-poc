
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "mydatabase")  # Add a database name here

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client[DB_NAME]
