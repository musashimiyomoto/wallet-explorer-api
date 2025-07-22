import re
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from enums.network import NetworkEnum


class WalletRequestCreate(BaseModel):
    address: str = Field(default=..., description="Wallet address")
    network: NetworkEnum = Field(default=NetworkEnum.TRON, description="Network type")

    @field_validator("address")
    def validate_address(cls, v):
        regex = {
            NetworkEnum.TRON: "^T[A-Za-z0-9]{33}$",
            NetworkEnum.SOLANA: "^[1-9A-HJ-NP-Za-km-z]{32,44}$",
        }
        if not re.match(regex[v.network], v):
            raise ValueError("Invalid address format")
        return v


class WalletInfo(BaseModel):
    balance: Optional[Decimal] = Field(None, description="Balance", ge=0)
    bandwidth: Optional[int] = Field(None, description="Bandwidth", ge=0)
    energy: Optional[int] = Field(None, description="Energy", ge=0)


class WalletRequestResponse(WalletInfo):
    id: int = Field(..., description="Request ID")
    network: NetworkEnum = Field(..., description="Network type")
    address: str = Field(..., description="Wallet address")
    created_at: datetime = Field(..., description="Request timestamp")

    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    limit: int = Field(default=10, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PaginatedWalletRequestResponse(BaseModel):
    items: List[WalletRequestResponse] = Field(
        ..., description="List of wallet requests"
    )
    total: int = Field(..., description="Total number of items", ge=0)
    page: int = Field(..., description="Current page", ge=1)
    limit: int = Field(..., description="Items per page", ge=1)
    pages: int = Field(..., description="Total number of pages", ge=1)

    @classmethod
    def create(
        cls, items: List[WalletRequestResponse], total: int, page: int, limit: int
    ) -> "PaginatedWalletRequestResponse":
        pages = (total + limit - 1) // limit if total > 0 else 1
        return cls(items=items, total=total, page=page, limit=limit, pages=pages)
