"""
Authentication API Routes
==========================
API endpoints for user authentication and authorization.
"""

import hashlib
import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr

# Define models locally to avoid import issues
class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    role: str = "user"

# Import settings
try:
    from config.settings import (
        JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS,
        DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD
    )
except ImportError:
    JWT_SECRET_KEY = "acds-secret-key"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    DEFAULT_ADMIN_EMAIL = "admin@acds.com"
    DEFAULT_ADMIN_PASSWORD = "admin123"

router = APIRouter(prefix="/auth", tags=["Authentication"])

# In-memory user store (use database in production)
users_db = {
    DEFAULT_ADMIN_EMAIL: {
        "id": "admin-001",
        "email": DEFAULT_ADMIN_EMAIL,
        "name": "System Administrator",
        "role": "admin",
        "password_hash": hashlib.sha256(DEFAULT_ADMIN_PASSWORD.encode()).hexdigest(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_login": None
    }
}

# Active tokens store
active_tokens = {}


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(user_id: str, email: str, role: str) -> tuple:
    """Create a JWT token."""
    expiration = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": expiration,
        "iat": datetime.now(timezone.utc)
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token, expiration


def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return the payload."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def get_current_user(authorization: str = Header(None)):
    """Dependency to get current authenticated user."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication header")
    
    token = parts[1]
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_email = payload.get("email")
    if user_email not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    
    return users_db[user_email]


@router.post("/login")
async def login(credentials: UserLogin):
    """
    Authenticate user and return access token.
    
    Use email and password to authenticate.
    Returns JWT token for subsequent API calls.
    """
    email = credentials.email.lower()
    
    # Check if user exists
    if email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user = users_db[email]
    
    # Verify password
    password_hash = hash_password(credentials.password)
    if password_hash != user["password_hash"]:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create token
    token, expiration = create_token(user["id"], user["email"], user["role"])
    
    # Store active token
    active_tokens[token] = {
        "user_id": user["id"],
        "expires": expiration.isoformat()
    }
    
    # Update last login
    users_db[email]["last_login"] = datetime.now(timezone.utc).isoformat()
    
    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "expires_in": JWT_EXPIRATION_HOURS * 3600,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
    }


@router.post("/logout")
async def logout(authorization: str = Header(None)):
    """
    Logout user and invalidate token.
    """
    if authorization:
        parts = authorization.split()
        if len(parts) == 2:
            token = parts[1]
            if token in active_tokens:
                del active_tokens[token]
    
    return {
        "success": True,
        "message": "Logged out successfully"
    }


@router.get("/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return {
        "success": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "created_at": user["created_at"],
            "last_login": user["last_login"]
        }
    }


@router.post("/register")
async def register_user(user_data: UserCreate, current_user: dict = Depends(get_current_user)):
    """
    Register a new user (admin only).
    """
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    email = user_data.email.lower()
    
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = {
        "id": f"user-{len(users_db) + 1:03d}",
        "email": email,
        "name": user_data.name,
        "role": user_data.role,
        "password_hash": hash_password(user_data.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_login": None
    }
    
    users_db[email] = new_user
    
    return {
        "success": True,
        "message": "User registered successfully",
        "user": {
            "id": new_user["id"],
            "email": new_user["email"],
            "name": new_user["name"],
            "role": new_user["role"]
        }
    }


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    user: dict = Depends(get_current_user)
):
    """
    Change current user's password.
    """
    # Verify current password
    if hash_password(current_password) != user["password_hash"]:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    users_db[user["email"]]["password_hash"] = hash_password(new_password)
    
    return {
        "success": True,
        "message": "Password changed successfully"
    }


@router.post("/validate-token")
async def validate_token(authorization: str = Header(None)):
    """
    Validate a JWT token.
    """
    if not authorization:
        return {"valid": False, "reason": "No token provided"}
    
    parts = authorization.split()
    if len(parts) != 2:
        return {"valid": False, "reason": "Invalid header format"}
    
    token = parts[1]
    payload = verify_token(token)
    
    if not payload:
        return {"valid": False, "reason": "Invalid or expired token"}
    
    return {
        "valid": True,
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role"),
        "expires": payload.get("exp")
    }


@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_user)):
    """
    List all users (admin only).
    """
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users_list = []
    for email, user in users_db.items():
        users_list.append({
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "created_at": user["created_at"],
            "last_login": user["last_login"]
        })
    
    return {
        "success": True,
        "users": users_list,
        "count": len(users_list)
    }
