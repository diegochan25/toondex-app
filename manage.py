import asyncio
from datetime import date
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typer import Typer
from app.config.db import engine
from app.models.users import User, UserRole

app = Typer()
logger = logging.getLogger(__name__)

async def _new_user(email: str, password: str, role: UserRole):
    async with AsyncSession(engine) as session:
        try:
            result = await session.execute(select(User).where(User.email == email))
            if result.scalar_one_or_none() is not None:
                logger.warning(f"User with email '{email}' already exists.")
                return
            unix = date(1970, 1, 1)
            session.add(User(email=email, password=password, role=role, birthdate=unix))
            await session.flush()
            await session.commit()
        except Exception as e:
            logger.exception(e)
            await session.rollback()

@app.command('createuser')
def create_user(email: str, password: str):
    return asyncio.run(_new_user(email, password, UserRole.Reader))


@app.command('createsuperuser')
def create_superuser(email: str, password: str):
    return asyncio.run(_new_user(email, password, UserRole.Admin))


@app.command('makemigrations')
def make_migrations():
    pass


@app.command('migrate')
def migrate():
    pass


if __name__ == '__main__':
    app()