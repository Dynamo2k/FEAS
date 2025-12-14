from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter(prefix="/profile", tags=["profile"])

mock_profile = {
    "name": "FEAS User",
    "email": "user@example.com",
    "role": "analyst",
    "bio": "Forensics and evidence analysis."
}

@router.get("/")
async def get_profile():
    return mock_profile

@router.patch("/")
async def update_profile(name: Optional[str] = None, bio: Optional[str] = None):
    if name:
        mock_profile["name"] = name
    if bio:
        mock_profile["bio"] = bio
    return {"ok": True, "profile": mock_profile}