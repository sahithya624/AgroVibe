from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

from backend.services import auth_service
from backend.api.deps import oauth2_scheme, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/signup")
async def signup(user_data: UserSignUp):
    """Register a new user account."""
    result = await auth_service.sign_up_user(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    return result

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """Authenticate user and return access token."""
    result = await auth_service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result["error"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result

@router.get("/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    """Get details of the currently authenticated user."""
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
