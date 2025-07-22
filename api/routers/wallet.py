from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db, wallet
from schemas import (
    SortingAndPaginationParams,
    WalletRequest,
    WalletResponse,
)
from schemas.common import PaginatedResponse

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.post(path="", summary="Get wallet info")
async def get_wallet_info(
    data: WalletRequest = Body(default=..., description="Wallet request data"),
    session: AsyncSession = Depends(db.get_session),
    usecase: wallet.WalletUsecase = Depends(wallet.get_wallet_usecase),
) -> WalletResponse:
    return await usecase.get_wallet_info(session=session, data=data)


@router.get(path="/requests", summary="Get wallet requests")
async def get_wallet_requests(
    data: SortingAndPaginationParams = Query(default=..., description="Pagination data"),
    session: AsyncSession = Depends(db.get_session),
    usecase: wallet.WalletUsecase = Depends(wallet.get_wallet_usecase),
) -> PaginatedResponse[WalletResponse]:
    return await usecase.get_paginated(session=session, data=data)
