from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func

from models.base import Base


class CoingeckoRatings(Base):
    __tablename__ = 'coingecko_ratings'

    coin_id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    watchlist_portfolio_users: Mapped[Optional[float]] = mapped_column()
    coingecko_score: Mapped[Optional[float]] = mapped_column()
    developer_score: Mapped[Optional[float]] = mapped_column()
    community_score: Mapped[Optional[float]] = mapped_column()
    liquidity_score: Mapped[Optional[float]] = mapped_column()
    public_interest_score: Mapped[Optional[float]] = mapped_column()
