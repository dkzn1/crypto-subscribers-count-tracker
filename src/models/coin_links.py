from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func


from models.base import Base


class CoinSocialMediaLinks(Base):
    __tablename__ = 'coin_social_media_links'

    coin_id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    reddit: Mapped[Optional[str]] = mapped_column()
    telegram: Mapped[Optional[str]] = mapped_column()
    discord: Mapped[Optional[str]] = mapped_column()
    twitter: Mapped[Optional[str]] = mapped_column()


class CoinHomepageLink(Base):
    __tablename__ = 'coin_homepage_links'

    id: Mapped[int] = mapped_column(primary_key=True)
    coin_id: Mapped[str] = mapped_column(String(length=50))
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    homepage_url: Mapped[str] = mapped_column()


class CoinGithubLink(Base):
    __tablename__ = 'coin_github_links'

    id: Mapped[int] = mapped_column(primary_key=True)
    coin_id: Mapped[str] = mapped_column(String(length=50))
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    github_url: Mapped[str] = mapped_column()
