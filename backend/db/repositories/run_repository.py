from datetime import datetime
from bson import ObjectId
from db.mongo import mongo_manager


class RunRepository:

    @staticmethod
    async def create_run(original_prompt: str, model_used: str):
        doc = {
            "original_prompt": original_prompt,
            "final_prompt": None,
            "final_response": None,
            "iterations": [],
            "model_used": model_used,
            "created_at": datetime.utcnow()
        }

        result = await mongo_manager.db.runs.insert_one(doc)
        return str(result.inserted_id)

    @staticmethod
    async def add_iteration(run_id: str, iteration_data: dict):
        await mongo_manager.db.runs.update_one(
            {"_id": ObjectId(run_id)},
            {"$push": {"iterations": iteration_data}}
        )

    @staticmethod
    async def finalize_run(run_id: str, final_prompt: str, final_response: str):
        await mongo_manager.db.runs.update_one(
            {"_id": ObjectId(run_id)},
            {
                "$set": {
                    "final_prompt": final_prompt,
                    "final_response": final_response
                }
            }
        )

    @staticmethod
    async def get_run(run_id: str):
        doc = await mongo_manager.db.runs.find_one(
            {"_id": ObjectId(run_id)}
        )
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    @staticmethod
    async def list_runs():
        runs = []
        cursor = mongo_manager.db.runs.find().sort("created_at", -1)
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            runs.append(doc)
        return runs