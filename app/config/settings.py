from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)

    python_env: Literal['development', 'testing', 'staging', 'production']

    secret_key: str

    app_host: str
    app_port: int
    log_level: Literal['debug', 'trace', 'info', 'warn', 'warning', 'error', 'fatal', 'critical']

    db_driver: str = 'postgresql+asyncpg'
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str
    s3_secure: bool = True

    access_control_allow_origins: str
    access_control_allow_methods: str
    access_control_allow_headers: str
    access_control_allow_credentials: bool

    trust_proxy: bool

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name
        )

    @property
    def allowed_origins(self) -> list[str]:
        origins = self.access_control_allow_origins.strip()
        return [o.strip() for o in origins.split(',') if o.strip()]

    @property
    def allowed_methods(self) -> list[str]:
        methods = self.access_control_allow_methods.strip()
        return [m.strip() for m in methods.split(',') if m.strip()]

    @property
    def allowed_headers(self) -> list[str]:
        headers = self.access_control_allow_headers.strip()
        return [h.strip() for h in headers.split(',') if h.strip()]

    @property
    def allow_credentials(self) -> bool:
        return self.access_control_allow_credentials


@lru_cache
def get_settings() -> Settings:
    return Settings()