"""
Authentication Service for SmartFarmingAI
Handles user registration, login, and JWT management.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from supabase import create_client, Client

from backend.config import settings

logger = logging.getLogger(__name__)

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Initialize Supabase client if configured
supabase: Optional[Client] = None
if settings.SUPABASE_URL and settings.SUPABASE_KEY and settings.ENABLE_REAL_DB:
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        logger.info("Supabase client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")

# In-memory mock user database for development
mock_users_db = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def sign_up_user(email: str, password: str, full_name: str) -> Dict[str, Any]:
    """Register a new user."""
    hashed_password = get_password_hash(password)
    
    if supabase and settings.ENABLE_REAL_DB:
        try:
            # Sign up with Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": {"full_name": full_name}}
            })
            
            if auth_response.user:
                return {
                    "success": True,
                    "user": {
                        "id": auth_response.user.id,
                        "email": email,
                        "full_name": full_name
                    }
                }
            return {"success": False, "error": "Registration failed"}
        except Exception as e:
            logger.error(f"Supabase sign-up error: {e}")
            return {"success": False, "error": str(e)}
    else:
        # Development mode: Mock database
        if email in mock_users_db:
            return {"success": False, "error": "User already exists"}
        
        user_id = f"user_{len(mock_users_db) + 1}"
        mock_users_db[email] = {
            "id": user_id,
            "email": email,
            "password": hashed_password,
            "full_name": full_name
        }
        
        logger.info(f"Registered mock user: {email}")
        return {
            "success": True,
            "user": {
                "id": user_id,
                "email": email,
                "full_name": full_name
            }
        }

async def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticate user and return access token."""
    if supabase and settings.ENABLE_REAL_DB:
        try:
            # Login with Supabase Auth
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                access_token = create_access_token(data={"sub": email, "id": auth_response.user.id})
                return {
                    "success": True,
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": auth_response.user.id,
                        "email": email,
                        "full_name": auth_response.user.user_metadata.get("full_name", "")
                    }
                }
            return {"success": False, "error": "Invalid email or password"}
        except Exception as e:
            logger.error(f"Supabase login error: {e}")
            return {"success": False, "error": str(e)}
    else:
        # Development mode: Mock database
        user = mock_users_db.get(email)
        if not user or not verify_password(password, user["password"]):
            return {"success": False, "error": "Invalid email or password"}
        
        access_token = create_access_token(data={"sub": email, "id": user["id"]})
        return {
            "success": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": email,
                "full_name": user["full_name"]
            }
        }

async def get_current_user(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return user details."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        
        if supabase and settings.ENABLE_REAL_DB:
            # In production, we'd verify with Supabase or DB
            return {"email": email, "id": payload.get("id")}
        else:
            user = mock_users_db.get(email)
            if user:
                return {"email": email, "id": user["id"], "full_name": user["full_name"]}
            return {"email": email, "id": payload.get("id")}
    except JWTError:
        return None
