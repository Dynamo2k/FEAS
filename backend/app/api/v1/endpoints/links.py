from fastapi import APIRouter, HTTPException
from typing import List, Optional

router = APIRouter(prefix="/links", tags=["links"])

@router.get("/", response_model=List[str])
async def list_links(q: Optional[str] = None):
    # Placeholder: In production, fetch from DB/service
    data = [
        "https://example.com",
        "https://github.com/Dynamo2k/FEAS",
        "https://docs.example.com",
    ]
    if q:
        data = [d for d in data if q.lower() in d.lower()]
    return data

@router.post("/", status_code=201)
async def add_link(url: str):
    if not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(status_code=400, detail="Invalid URL")
    # TODO: persist
    return {"ok": True, "url": url}