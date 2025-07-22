from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import WalletRequestRepository


class WalletRequestUsecase:
    def __init__(self):
        self._wallet_request_repository = WalletRequestRepository()
