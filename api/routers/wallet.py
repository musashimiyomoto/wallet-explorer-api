from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db, wallet
from enums.network import NetworkEnum
from schemas import (
    SortingAndPaginationParams,
    WalletInfo,
    WalletRequest,
    WalletResponse,
)
from schemas.common import PaginatedResponse
from tasks.wallet import save_wallet_info

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.post(path="", summary="Get wallet info")
async def get_wallet_info(
    network: Annotated[NetworkEnum, Depends(wallet.get_network)],
    data: Annotated[WalletRequest, Body(description="Wallet request data")],
    usecase: Annotated[wallet.WalletUsecase, Depends(wallet.get_wallet_usecase)],
) -> WalletInfo:
    wallet_info = await usecase.get_wallet_info(address=data.address)
    await save_wallet_info.kiq(
        network=network, wallet_info=wallet_info.model_dump(mode="json")
    )
    return wallet_info


@router.get(path="/history", summary="Get wallet history")
async def get_wallet_history(
    data: Annotated[SortingAndPaginationParams, Depends(SortingAndPaginationParams)],
    session: Annotated[AsyncSession, Depends(db.get_session)],
    usecase: Annotated[wallet.WalletUsecase, Depends(wallet.get_wallet_usecase)],
) -> PaginatedResponse[WalletResponse]:
    return await usecase.get_history(session=session, data=data)
