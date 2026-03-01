import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from fastapi import FastAPI
from db.mongo import connect_to_mongo, close_mongo_connection
from api.optimize import router as optimize_router
from api.health import router as health_router
from api.auth import router as auth_router


app = FastAPI(title="SRPP Studio Backend")


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


app.include_router(optimize_router)
app.include_router(health_router)
app.include_router(auth_router)