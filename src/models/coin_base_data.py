from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func


from models.base import Base


class CoinBaseData(Base):
    __tablename__ = 'coin_base_data'

    coin_id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    symbol: Mapped[Optional[str]] = mapped_column(String(length=10))
    name: Mapped[Optional[str]] = mapped_column(String(length=100))
    categories: Mapped[Optional[str]] = mapped_column()
