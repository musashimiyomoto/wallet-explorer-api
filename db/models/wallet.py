from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DECIMAL,
    CheckConstraint,
    DateTime,
    Enum,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from constants.db import TEXT_LENGTH
from db.models.base import Base
from enums.network import NetworkEnum


class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = (
        CheckConstraint("balance >= 0", name="check_balance_positive"),
        CheckConstraint("bandwidth >= 0", name="check_bandwidth_positive"),
        CheckConstraint("energy >= 0", name="check_energy_positive"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="Wallet ID"
    )

    network: Mapped[NetworkEnum] = mapped_column(
        Enum(NetworkEnum), nullable=False, index=True, comment="Network"
    )
    address: Mapped[str] = mapped_column(
        String(TEXT_LENGTH), nullable=False, index=True, comment="Wallet address"
    )

    balance: Mapped[Decimal | None] = mapped_column(
        DECIMAL(18, 6), nullable=True, comment="Wallet balance"
    )
    bandwidth: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="Wallet bandwidth"
    )
    energy: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="Wallet energy"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Created at"
    )

    def __repr__(self) -> str:
        return (
            f"<Wallet(id={self.id}, "
            f"network='{self.network}', "
            f"address='{self.address}', "
            f"created_at='{self.created_at}')>"
        )
