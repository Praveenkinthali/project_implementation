from fastapi import APIRouter, HTTPException
from models.user_model import UserCreate, UserLogin
from db.repositories.user_repository import UserRepository
from utils.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserCreate):

    existing = await UserRepository.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    user_id = await UserRepository.create_user({
        "name": user.name,
        "email": user.email,
        "password": hashed
    })

    return {"message": "User created", "user_id": user_id}


@router.post("/login")
async def login(user: UserLogin):

    db_user = await UserRepository.get_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user["email"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }