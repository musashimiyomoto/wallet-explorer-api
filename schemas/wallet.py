import re
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from constants.network import NETWORK_REGEX
from enums.network import NetworkEnum


class WalletRequest(BaseModel):
    address: str = Field(default=..., description="Wallet address")
    network: NetworkEnum = Field(default=NetworkEnum.TRON, description="Network type")

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str, info: ValidationInfo) -> str:
        regex = NETWORK_REGEX.get(info.data.get("network"))

        if not regex:
            raise ValueError("Invalid network")

        if not re.match(regex, value):
            raise ValueError("Invalid address format")

        return value


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
