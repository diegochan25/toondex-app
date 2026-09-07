from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID as SQLUUID, DateTime, Index, String, Text, func
from app.core.utils import utcnow
from app.models.base import Base
from app.services import password

class User(Base):
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def password(self) -> str:
        raise AttributeError(f"Property {self.__class__.__name__}.password is write-only.")

    @password.setter
    def password(self, value: str):
        self.password_hash = password.hash(value)

    profile: Mapped['UserProfile'] = relationship(back_populates='user')
    settings: Mapped['UserSettings'] = relationship(back_populates='user')


class UserProfile(Base):
    user: Mapped['User'] = relationship(back_populates='profile')

    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    profile_picture_url: Mapped[str | None] = mapped_column(String)
    bio: Mapped[str | None] = mapped_column(Text)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def created_at(self) -> datetime:
        return self.user.created_at

    social_handles: Mapped[list['UserSocialHandle']] = relationship(back_populates='profile') 


class UserSocialHandle(Base):
    __table_args__ = (
        Index('uniq_url_per_platform', 'platform', 'url', unique=True),
    )
    profile: Mapped['UserProfile'] = relationship(back_populates='social_handles')

    platform: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)

class UserSettings(Base):
    user: Mapped['User'] = relationship(back_populates='settings')

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def created_at(self) -> datetime:
        return self.user.created_at
 