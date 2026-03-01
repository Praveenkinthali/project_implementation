from fastapi import APIRouter, HTTPException
from db.repositories.user_repository import UserRepository
from models.auth_models import RegisterRequest, LoginRequest, TokenResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):

    existing = await UserRepository.get_by_email(request.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = AuthService.hash_password(request.password)

    user_id = await UserRepository.create_user(
        request.email,
        hashed,
        provider="local"
    )

    token = AuthService.create_access_token({"sub": user_id})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):

    user = await UserRepository.get_by_email(request.email)

    if not user or not AuthService.verify_password(
        request.password,
        user["hashed_password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = AuthService.create_access_token({"sub": str(user["_id"])})

    return {"access_token": token, "token_type": "bearer"}