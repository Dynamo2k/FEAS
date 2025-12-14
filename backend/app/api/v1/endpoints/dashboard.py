from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/dashboard", tags=["dashboard"]) 

@router.get("/cards", response_model=List[dict])
async def get_cards():
    return [
        {"title": "Jobs", "value": 12, "trend": "+3%"},
        {"title": "Evidence", "value": 47, "trend": "+1%"},
        {"title": "Reports", "value": 8, "trend": "-2%"},
    ]

@router.get("/activity", response_model=List[dict])
async def get_activity():
    return [
        {"event": "upload", "subject": "image.png", "by": "system", "ts": "2025-12-14T09:30:00Z"},
        {"event": "report", "subject": "case-123.pdf", "by": "analyst", "ts": "2025-12-14T10:05:00Z"},
    ]