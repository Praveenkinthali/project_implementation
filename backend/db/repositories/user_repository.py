from datetime import datetime
from bson import ObjectId
from db.mongo import mongo_manager


class UserRepository:

    @staticmethod
    async def create_user(email: str, hashed_password: str, provider: str):
        doc = {
            "email": email,
            "hashed_password": hashed_password,
            "auth_provider": provider,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow()
        }

        result = await mongo_manager.db.users.insert_one(doc)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_email(email: str):
        return await mongo_manager.db.users.find_one({"email": email})

    @staticmethod
    async def update_last_login(user_id: str):
        await mongo_manager.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login": datetime.utcnow()}}
        )