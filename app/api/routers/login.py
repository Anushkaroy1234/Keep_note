from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schema.login import Userdetails,Userinfo,PasswordUpdate
from app.crud.login import create_user,check_user
from app.core.security import create_access_token,create_refresh_token
router=APIRouter()

@router.get('/')
async def hello():
    return "Hello"

@router.post('/signup')
async def create_user_endpoint(userdetails:Userdetails, db: AsyncSession = Depends(get_db)):
    try:
        return await create_user(db, userdetails)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(userinfo: Userinfo, db: AsyncSession = Depends(get_db)):
    db_user = await check_user(db, userinfo)   # Check email + password
    token_data = {"user_id": db_user.id, "email": db_user.email}
    access_token = create_access_token(token_data)   # JWT creation
    refresh_token = create_refresh_token(token_data) # JWT creation
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.put('/login_update')
async def update_info(pass_update:PasswordUpdate):
    pass
