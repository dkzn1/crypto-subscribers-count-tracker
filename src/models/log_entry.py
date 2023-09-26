from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String
from sqlalchemy.sql import func

from models.base import Base


class LogEntry(Base):
    __tablename__ = 'logs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    level: Mapped[str] = mapped_column(String(length=20))
    name: Mapped[str] = mapped_column(String(length=40))
    message: Mapped[str] = mapped_column()
