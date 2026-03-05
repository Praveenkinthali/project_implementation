from bson import ObjectId
from db.mongo import mongo_manager


class UserRepository:

    @staticmethod
    async def get_by_email(email: str):
        return await mongo_manager.db.users.find_one({"email": email})

    @staticmethod
    async def create_user(user_data: dict):
        result = await mongo_manager.db.users.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(user_id: str):
        return await mongo_manager.db.users.find_one({"_id": ObjectId(user_id)})