from fastapi import APIRouter, HTTPException
from typing import List, Optional

router = APIRouter(prefix="/social", tags=["social"])

mock_social = [
    {"platform": "twitter", "handle": "@feas", "url": "https://twitter.com/feas"},
    {"platform": "linkedin", "handle": "FEAS", "url": "https://linkedin.com/company/feas"},
]

@router.get("/", response_model=List[dict])
async def list_social(q: Optional[str] = None):
    data = mock_social
    if q:
        data = [d for d in data if q.lower() in d["platform"].lower() or q.lower() in d["handle"].lower()]
    return data

@router.post("/", status_code=201)
async def add_social(platform: str, handle: str, url: str):
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")
    item = {"platform": platform, "handle": handle, "url": url}
    # TODO: persist
    return {"ok": True, "social": item}