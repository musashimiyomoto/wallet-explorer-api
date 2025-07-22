from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db, wallet
from schemas import (
    SortingAndPaginationParams,
    WalletInfo,
    WalletRequest,
    WalletResponse,
)
from schemas.common import PaginatedResponse

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.post(path="", summary="Get wallet info")
async def get_wallet_info(
    background_tasks: BackgroundTasks,
    data: Annotated[WalletRequest, Body(description="Wallet request data")],
    session: Annotated[AsyncSession, Depends(db.get_session)],
    usecase: Annotated[wallet.WalletUsecase, Depends(wallet.get_wallet_usecase)],
) -> WalletInfo:
    wallet_info = await usecase.get_wallet_info(address=data.address)
    background_tasks.add_task(
        usecase.save_wallet_info, session=session, wallet_info=wallet_info
    )
    return wallet_info


@router.get(path="/history", summary="Get wallet history")
async def get_wallet_history(
    data: Annotated[SortingAndPaginationParams, Depends(SortingAndPaginationParams)],
    session: Annotated[AsyncSession, Depends(db.get_session)],
    usecase: Annotated[wallet.WalletUsecase, Depends(wallet.get_wallet_usecase)],
) -> PaginatedResponse[WalletResponse]:
    return await usecase.get_history(session=session, data=data)
