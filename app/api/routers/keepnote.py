'''get(note),post(new note ), put(update(note progress))'''

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy import select
from app.schema.note import KeepNote
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schema.note import KeepNote
from app.crud.keepnote import create_note,update_note
from app.core.security import get_current_user
router=APIRouter()


@router.get('/keep_note')
async def getnote(notes:KeepNote, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    pass


@router.post('/keep_note')
async def postnote(notes:KeepNote, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    try:
        return await create_note(db, notes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put('/keep_note')
async def updatenote(notes:KeepNote, db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    try:
        return await update_note(db, notes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
