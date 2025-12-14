from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db.session import get_db
from app.models.sql_models import UserProfile

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Security Configuration
# WARNING: Change these values in production!
# Load SECRET_KEY from environment variables in production
SECRET_KEY = "your-secret-key-here-change-in-production"  # TODO: Use env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Schemas
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "Analyst"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    bio: str

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Note: For demo/MVP, we'll store password hash in UserProfile
# In production, create a separate User table with proper authentication fields
# WARNING: This is a simplified demo implementation - NOT for production use!

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    WARNING: This is a demo/development implementation.
    In production:
    1. Create a separate User table with password_hash column
    2. Properly hash and store passwords
    3. Add email verification
    4. Implement rate limiting
    """
    # Check if email already exists
    existing = db.query(UserProfile).filter(UserProfile.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    # NOTE: Not storing password for demo - this is intentional for MVP/development
    new_user = UserProfile(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        bio=f"Digital forensics {user_data.role.lower()}",
    )
    
    # For demo purposes, we'll store a reference to password in a simple way
    # This is NOT secure for production - just for demo/development
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email, "id": new_user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role,
            "bio": new_user.bio
        }
    }

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login with email and password
    
    WARNING: This is a demo/development implementation.
    For development/testing purposes, this accepts any login and creates users on-the-fly.
    
    In production:
    1. Verify password against stored hash
    2. Add account lockout after failed attempts
    3. Implement rate limiting
    4. Add 2FA support
    """
    
    user = db.query(UserProfile).filter(UserProfile.email == form_data.username).first()
    
    if not user:
        # For demo/development: Create user on first login if doesn't exist
        # WARNING: This is intentionally insecure for development/testing only
        user = UserProfile(
            name="Investigator",
            email=form_data.username,
            role="Senior Analyst",
            bio="Digital forensics specialist"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "bio": user.bio
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current logged-in user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(UserProfile).filter(UserProfile.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/logout")
async def logout():
    """Logout (client-side token removal)"""
    return {"message": "Successfully logged out"}
