from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from enums.network import NetworkEnum


class WalletRequest(BaseModel):
    address: str = Field(default=..., description="Wallet address")


class WalletInfo(BaseModel):
    balance: Decimal | None = Field(default=None, description="Balance", ge=0)
    bandwidth: int | None = Field(default=None, description="Bandwidth", ge=0)
    energy: int | None = Field(default=None, description="Energy", ge=0)


class WalletResponse(WalletInfo):
    id: int = Field(default=..., description="Request ID")
    network: NetworkEnum = Field(default=..., description="Network type")
    address: str = Field(default=..., description="Wallet address")
    created_at: datetime = Field(default=..., description="Request timestamp")

    class Config:
        from_attributes = True
