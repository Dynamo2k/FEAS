from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.sql_models import UserProfile

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None

@router.get("/")
async def get_profile(db: Session = Depends(get_db)):
    # Retrieve the first user, or create default if none exists
    profile = db.query(UserProfile).first()
    if not profile:
        profile = UserProfile()
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return {
        "name": profile.name,
        "email": profile.email,
        "role": profile.role,
        "bio": profile.bio
    }

@router.patch("/")
async def update_profile(data: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).first()
    if not profile:
        profile = UserProfile()
        db.add(profile)
    
    if data.name: profile.name = data.name
    if data.bio: profile.bio = data.bio
    if data.email: profile.email = data.email
    
    db.commit()
    return {"ok": True, "profile": profile}
