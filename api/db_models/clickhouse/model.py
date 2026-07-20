from datetime import datetime

import sqlalchemy as sa
from clickhouse_sqlalchemy import engines, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Log(Base):
    __tablename__ = "logs"

    timestamp: Mapped[datetime] = mapped_column(
        types.DateTime64, primary_key=True
    )
    source: Mapped[str] = mapped_column(types.String, primary_key=True)
    level: Mapped[str] = mapped_column(types.String, nullable=False)
    message: Mapped[str] = mapped_column(types.String, nullable=False)

    __table_args__ = (
        engines.MergeTree(
            order_by=("timestamp", "source"),
        ),
    )
