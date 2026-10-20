from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database():
    if db.client is not None:
        try:
            return db.client[settings.DATABASE_NAME]
        except Exception:
            return None
    return None

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"Connected to MongoDB at {settings.MONGODB_URL}")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB Connection")
