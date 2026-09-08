from logging import getLogger
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db import engine
from app.config.settings import Settings, get_settings
from app.schemas.internal import ClientInfo, PaginationParams


logger = getLogger(__name__)

settings = get_settings()

async def get_session():
    try:
        async with AsyncSession(engine) as session:
            yield session
            await session.commit()
    except Exception as e:
        logger.exception(e)
        await session.rollback()

async def get_client_info(request: Request):
    if settings.trust_proxy:
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            ip_address = forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.headers.get('x-real-ip')
    else:
        ip_address = request.client.host if request.client else None

    user_agent = request.headers.get('user-agent')

    return ClientInfo(ip_address=ip_address, user_agent=user_agent)


async def get_pagination(request: Request):
    page = request.query_params.get('page')
    limit = request.query_params.get('limit')
    return PaginationParams(page=page, limit=limit)


RequiresDB = Annotated[AsyncSession, Depends(get_session)]

RequiresSettings = Annotated[Settings, Depends(get_settings)]

RequiresClientInfo = Annotated[ClientInfo, Depends(get_client_info)]

RequiresPagination = Annotated[PaginationParams, Depends(get_pagination)]