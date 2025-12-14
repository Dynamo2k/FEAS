from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.links import router as links_router
from app.api.v1.endpoints.social import router as social_router
from app.api.v1.endpoints.profile import router as profile_router
from app.api.v1.endpoints.dashboard import router as dashboard_router

app = FastAPI(title="FEAS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Root
@app.get("/")
async def root():
    return {"name": "FEAS", "version": "1.0.0"}

# Routers
app.include_router(links_router)
app.include_router(social_router)
app.include_router(profile_router)
app.include_router(dashboard_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
