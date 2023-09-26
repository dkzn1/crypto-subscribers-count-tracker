from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func

from .base import Base


class Stablecoin(Base):
    __tablename__ = 'stablecoins'

    coin_id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
