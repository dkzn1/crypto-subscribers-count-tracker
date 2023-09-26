from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func


from models.base import Base


class CoinSubscriberTrends(Base):
    __tablename__ = 'coin_subscriber_trends'

    coin_id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    days_3: Mapped[Optional[float]] = mapped_column()
    days_7: Mapped[Optional[float]] = mapped_column()
    days_14: Mapped[Optional[float]] = mapped_column()
    days_30: Mapped[Optional[float]] = mapped_column()
    days_60: Mapped[Optional[float]] = mapped_column()
    days_90: Mapped[Optional[float]] = mapped_column()
