from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User

async def find_by_id(db: AsyncSession, id: UUID) -> User | None:
    stmt = select(User).where(User.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def exists_by_email(db: AsyncSession, email: str) -> bool:
    stmt = select(1).select_from(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None

async def all(db: AsyncSession, limit: int = 20, offset: int = 0) -> list[User]:
    stmt = select(User).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())