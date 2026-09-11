from datetime import datetime
from dateutil.relativedelta import relativedelta
from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID as SQLUUID, Boolean, Date, DateTime, Enum, ForeignKey, Index, String, Text, func
from sqlalchemy.ext.hybrid import hybrid_property as hybridproperty, hybrid_method as hybridmethod
from app.core.utils import utcnow
from app.models.base import Base
from app.models.locales import SupportedLanguages
from app.services import password, storage

if TYPE_CHECKING:
    from app.models.series import Series

class UserRoles(StrEnum):
    Reader = 'reader'
    Creator = 'creator'
    Staff = 'staff'
    Admin = 'admin'

class UserGenders(StrEnum):
    Male = 'male'
    Female = 'female'
    Other = 'other'
    RatherNotSay = 'rather not say'

class AppThemes(StrEnum):
    Light = 'light'
    Dark = 'dark'
    System = 'system'

class HorizontalContent(StrEnum):
    LTR = 'left-to-right'
    RTL = 'right-to-left'
    TTB = 'top-to-bottom'

class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    email_address: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), default=UserRoles.Reader)
    birthdate: Mapped[datetime] = mapped_column(Date())
    otp: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @hybridproperty
    def email(self) -> str:
        return self.email_address

    @email.setter
    def email(self, value: str):
        self.email_address = value.strip().lower()

    @property
    def password(self) -> str:
        raise AttributeError(f"Property {self.__class__.__name__}.password is write-only.")

    @password.setter
    def password(self, value: str):
        self.password_hash = password.hash(value)

    def authenticate(self, raw: str) -> bool:
        return password.verify(raw, self.password_hash)

    @hybridmethod
    def is_18(self) -> bool:
        return self.birthdate <= utcnow().date() - relativedelta(years=18)

    profile: Mapped['UserProfile'] = relationship(back_populates='user')
    settings: Mapped['UserSettings'] = relationship(back_populates='user')
    works: Mapped[list['Series']] = relationship(back_populates='author')


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='profile')

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    profile_picture_key: Mapped[str | None] = mapped_column(String)
    bio: Mapped[str | None] = mapped_column(Text)
    gender: Mapped[UserGenders | None] = mapped_column(Enum(UserGenders))

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def created_at(self) -> datetime:
        return self.user.created_at

    @property
    def profile_picture(self) -> str:
        return storage.presign_get(self.profile_picture_key)

    @property
    def full_name(self) -> str:
        return ' '.join([w.strip() for w in [self.first_name, self.last_name] if w and w.strip()])

    social_handles: Mapped[list['UserSocialHandle']] = relationship(back_populates='profile') 


class UserSocialHandle(Base):
    __tablename__ = 'user_social_handles'
    __table_args__ = (
        Index('uniq_url_per_platform', 'platform', 'url', unique=True),
    )

    profile_id: Mapped[UUID] = mapped_column(ForeignKey('user_profiles.id', ondelete='CASCADE'))
    profile: Mapped['UserProfile'] = relationship(back_populates='social_handles')

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    platform: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    

class UserSettings(Base):
    __tablename__ = 'user_settings'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='settings')

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    content_language: Mapped[SupportedLanguages] = mapped_column(Enum(SupportedLanguages), default=SupportedLanguages.English)
    ui_language: Mapped[SupportedLanguages] = mapped_column(Enum(SupportedLanguages), default=SupportedLanguages.English)
    theme: Mapped[AppThemes] = mapped_column(Enum(AppThemes), default=AppThemes.System)
    horizontal_content_navigation: Mapped[HorizontalContent] = mapped_column(Enum(HorizontalContent), default=HorizontalContent.RTL)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def created_at(self) -> datetime:
        return self.user.created_at