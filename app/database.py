
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "mydatabase")  

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client[DB_NAME]

# Create TTL index on created_at field
async def create_ttl_index():
    try:
        await database['token'].create_index(
            "token",
            expireAfterSeconds=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",""))  # TTL in seconds (1 hour)
        )
    except:
        print("Already exist")