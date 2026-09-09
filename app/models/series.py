from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Table, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util import hybridmethod
from app.models.base import Base
from app.models.users import User
from app.services import storage

class CompletionStatus(StrEnum):
    Draft = 'draft'
    Preview = 'preview'
    Ongoing = 'ongoing'
    OnHiatus = 'on hiatus'
    Completed = 'completed'
    Canceled = 'canceled'


class ReadingDirection(StrEnum):
    Vertical = 'vertical'
    Horizontal = 'horizontal'


series_tag_associations = Table(
    'series_tag_associations',
    Base.metadata,
    Column('series_id', ForeignKey('series.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('series_tags.id', ondelete='CASCADE'), primary_key=True),
)

class Series(Base):
    __tablename__ = 'series'
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    author_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    author: Mapped[User] = relationship(back_populates='works')

    title: Mapped[str] = mapped_column(String, index=True)
    summary: Mapped[str] = mapped_column(Text)
    status: Mapped[CompletionStatus] = mapped_column(Enum(CompletionStatus), default=CompletionStatus.Draft)
    thumbnail_key: Mapped[str | None] = mapped_column(String)
    banner_key: Mapped[str | None] = mapped_column(String)
    reading_direction: Mapped[ReadingDirection] = mapped_column(Enum(ReadingDirection))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    collections: Mapped[list['SeriesCollection']] = relationship(back_populates='series')
    tags: Mapped[list['SeriesTag']] = relationship(secondary=series_tag_associations, back_populates='series')

    @property
    def thumbnail(self) -> str:
        return storage.presign_get(self.thumbnail_key)

    @property
    def banner(self) -> str:
        return storage.presign_get(self.banner_key)

    @hybridmethod
    def uses_default_collection(self) -> bool:
        return len(self.collections) == 1 and self.collections[0].default

class SeriesTag(Base):
    __tablename__ = 'series_tags'

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    tag_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    series: Mapped[list[Series]] = relationship(secondary=series_tag_associations, back_populates='tags')

class SeriesCollection(Base):
    __tablename__ = 'series_collections'

    series_id: Mapped[UUID] = mapped_column(ForeignKey('series.id', ondelete='CASCADE'))
    series: Mapped[Series] = relationship(back_populates='collections')
    
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    default: Mapped[bool] = mapped_column(Boolean, default=False)
    display_name: Mapped[str] = mapped_column(String)
    index: Mapped[int] = mapped_column(Integer, index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    thumbnail_key: Mapped[str | None] = mapped_column(String)
    banner_key: Mapped[str | None] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    episodes: Mapped[list['SeriesEpisode']] = relationship(back_populates='collection')

    @property
    def thumbnail(self) -> str:
        return storage.presign_get(self.thumbnail_key)

    @property
    def banner(self) -> str:
        return storage.presign_get(self.banner_key)

class SeriesEpisode(Base):
    __tablename__ = 'series_episodes'

    collection_id: Mapped[UUID] = mapped_column(ForeignKey('series_collections.id', ondelete='CASCADE'))
    collection: Mapped[SeriesCollection] = relationship(back_populates='episodes')

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    display_name: Mapped[str] = mapped_column(String)
    index: Mapped[int] = mapped_column(Integer, index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    thumbnail_key: Mapped[str | None] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    media: Mapped[list['EpisodeReaderMedia']] = relationship(back_populates='episode')

    @property
    def thumbnail(self) -> str:
        return storage.presign_get(self.thumbnail_key)


class EpisodeReaderMedia(Base):
    __tablename__ = 'episode_reader_media'

    episode_id: Mapped[UUID] = mapped_column(ForeignKey('series_episodes.id', ondelete='CASCADE'))
    episode: Mapped[SeriesEpisode] = relationship(back_populates='media')

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    key: Mapped[str] = mapped_column(String)
    index: Mapped[int] = mapped_column(Integer, index=True)

    @property
    def media(self) -> str:
        return storage.presign_get(self.key)