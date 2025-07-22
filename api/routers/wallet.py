from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db, wallet
from schemas.wallet import (
    PaginatedWalletRequestResponse,
    PaginationParams,
    WalletRequestCreate,
    WalletRequestResponse,
)

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.post(path="", summary="Get wallet info")
async def get_wallet_info(
    wallet_request: WalletRequestCreate,
    session: AsyncSession = Depends(db.get_session),
    usecase: wallet.WalletUsecase = Depends(wallet.get_wallet_usecase),
) -> WalletRequestResponse:
    return await usecase.get_wallet_info(
        session=session, request_data=wallet_request
    )


@router.get(path="/requests", summary="Get wallet requests")
async def get_wallet_requests(
    page: int = 1,
    limit: int = 10,
    session: AsyncSession = Depends(db.get_session),
    usecase: wallet.WalletUsecase = Depends(wallet.get_wallet_usecase),
) -> PaginatedWalletRequestResponse:
    pagination = PaginationParams(page=page, limit=limit)
    return await usecase.get_wallet_requests_paginated(
        session=session, pagination=pagination
    )
