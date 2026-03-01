from fastapi import APIRouter
from db.mongo import mongo_manager

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.get("/health/db")
async def db_health():
    try:
        await mongo_manager.client.admin.command("ping")
        return {"database": "connected"}
    except Exception:
        return {"database": "disconnected"}