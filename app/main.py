from fastapi import FastAPI,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.middleware.auth import AuthMiddleware
from app.api.routers.login import router as auth_router
from app.api.routers.keepnote import router as keepnote_router
from app.db.database import engine
from app.db.base import Base

app = FastAPI()

bearer_scheme = HTTPBearer()

@app.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Swagger will show a simple Authorize button with Bearer token input
    """
    return {
        "token_type": credentials.scheme,  # should be 'Bearer'
        "token": credentials.credentials
    }


app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Login"]
)

app.include_router(
    keepnote_router,
    prefix="/keep_note",
    tags=["Keep Notes"]
)

app.add_middleware(AuthMiddleware)

@app.on_event("startup")
async def startup():
    """Create tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

