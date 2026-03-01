from motor.motor_asyncio import AsyncIOMotorClient
from core.config import get_settings


class MongoManager:
    client: AsyncIOMotorClient = None
    db = None


mongo_manager = MongoManager()


async def connect_to_mongo():
    settings = get_settings()
    mongo_manager.client = AsyncIOMotorClient(settings.mongo_url)
    mongo_manager.db = mongo_manager.client["srpp_db"]
    print("✅ Connected to MongoDB")


async def close_mongo_connection():
    if mongo_manager.client:
        mongo_manager.client.close()
        print("❌ MongoDB connection closed")