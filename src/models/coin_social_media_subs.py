from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from models.base import Base


class CoinSocialMediaSubs(Base):
    __tablename__ = 'coin_social_media_subs'

    id: Mapped[str] = mapped_column(primary_key=True)
    coin_id: Mapped[str] = mapped_column(String(length=50), ForeignKey("coin_base_data.coin_id"))
    platform_name: Mapped[str] = mapped_column(String(length=100))
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    subscriber_count: Mapped[int] = mapped_column()
