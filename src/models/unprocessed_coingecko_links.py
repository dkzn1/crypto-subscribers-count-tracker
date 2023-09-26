from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func

from models.base import Base


class UnprocessedCoingeckoLinks(Base):
    __tablename__ = 'unprocessed_coingecko_links'

    coin_id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    links: Mapped[Optional[str]] = mapped_column()
