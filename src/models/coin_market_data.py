from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from models.base import Base


class CoinMarketData(Base):
    __tablename__ = 'coin_market_data'

    coin_id: Mapped[str] = mapped_column(String(length=50), primary_key=True)
    last_updated: Mapped[Optional[str]] = mapped_column()
    current_price: Mapped[Optional[float]] = mapped_column()
    market_cap: Mapped[Optional[float]] = mapped_column()
    market_cap_rank: Mapped[Optional[int]] = mapped_column()
    total_volume: Mapped[Optional[float]] = mapped_column()
    low_24h: Mapped[Optional[float]] = mapped_column()
    high_24h: Mapped[Optional[float]] = mapped_column()
    price_change_percentage_1h_in_currency: Mapped[Optional[float]] = mapped_column()
    price_change_percentage_24h_in_currency: Mapped[Optional[float]] = mapped_column()
    price_change_percentage_7d_in_currency: Mapped[Optional[float]] = mapped_column()
    price_change_percentage_14d_in_currency: Mapped[Optional[float]] = mapped_column()
    price_change_percentage_30d_in_currency: Mapped[Optional[float]] = mapped_column()
    price_change_percentage_200d_in_currency: Mapped[Optional[float]] = mapped_column()
    price_change_percentage_1y_in_currency: Mapped[Optional[float]] = mapped_column()
