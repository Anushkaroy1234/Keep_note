from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.keepnote import KeepNote
from app.schema.note import KeepNote as addnote
from app.core.security import hash_password,verify_password


async def create_note(db: AsyncSession, keep_note: addnote):
    db_note =KeepNote(**keep_note.model_dump())

    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


async def update_note(db: AsyncSession, keep_note: addnote):
    result = await db.execute(
        select(KeepNote).where(KeepNote.Title == keep_note.Title)
    )
    db_note = result.scalar_one_or_none()
    if not db_note:
        raise ValueError("Not present ")