import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from explorers.base import BaseExplorer
from repositories import WalletRepository
from schemas import (
    PaginatedResponse,
    SortingAndPaginationParams,
    WalletRequest,
    WalletResponse,
)

logger = logging.getLogger(__name__)


class WalletUsecase:
    def __init__(self, explorer: BaseExplorer):
        self._wallet_repository = WalletRepository()
        self._explorer = explorer

    async def get_wallet_info(
        self, session: AsyncSession, data: WalletRequest
    ) -> WalletResponse:
        if not self._explorer.is_valid_address(address=data.address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid address: {data.address}",
            )

        wallet_info = await self._explorer.get_wallet_info(address=data.address)

        return WalletResponse.model_validate(
            await self._wallet_repository.create(
                session=session,
                data={
                    "address": data.address,
                    "network": data.network,
                    "balance": wallet_info.balance,
                    "bandwidth": wallet_info.bandwidth,
                    "energy": wallet_info.energy,
                },
            )
        )

    async def get_paginated(
        self, session: AsyncSession, data: SortingAndPaginationParams
    ) -> PaginatedResponse[WalletResponse]:
        return PaginatedResponse(
            results=[
                WalletResponse.model_validate(item)
                for item in await self._wallet_repository.get_all(
                    session=session,
                    offset=data.offset,
                    limit=data.limit,
                    sort_by=data.sort_by,
                    sort_direction=data.sort_direction,
                )
            ],
            count=await self._wallet_repository.get_count(session=session),
            page=data.page,
            limit=data.limit,
        )
