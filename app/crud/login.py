from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.login import Userdetails
from app.schema.login import Userdetails as UserSchema,Userinfo
from app.core.security import hash_password,verify_password


async def create_user(db: AsyncSession, user_in: UserSchema):
    db_user = Userdetails(
        name=user_in.name,
        email=user_in.email,
        password=hash_password(user_in.password),
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def check_user(db: AsyncSession, user_in: Userinfo):
    result = await db.execute(
        select(Userdetails).where(Userdetails.email == user_in.email)
    )
    db_user = result.scalar_one_or_none()

    #  If user not found
    if not db_user:
        raise ValueError("Invalid email or password")

    #  2. Verify password
    if not verify_password(user_in.password, db_user.password):
        raise ValueError("Invalid email or password")

    #  Login success
    return db_user