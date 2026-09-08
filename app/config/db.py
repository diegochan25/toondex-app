from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import get_settings

settings = get_settings()

engine = create_async_engine(
    url=settings.db_url,
    echo=settings.python_env == 'development',
    pool_size=5,
    max_overflow=8,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args={
        'command_timeout': 60
    }
)