import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import WalletRequestRepository
from schemas.wallet import (
    PaginatedWalletRequestResponse,
    PaginationParams,
    WalletRequestCreate,
    WalletRequestResponse,
)
from explorers.base import BaseExplorer

logger = logging.getLogger(__name__)


class WalletUsecase:
    def __init__(self, explorer: BaseExplorer):
        self._wallet_request_repository = WalletRequestRepository()
        self._explorer = explorer

    async def get_wallet_info(
        self, session: AsyncSession, request_data: WalletRequestCreate
    ) -> WalletRequestResponse:
        address = request_data.address
        network = request_data.network

        logger.info(f"Getting wallet info for address: {address}")

        # Проверяем валидность адреса
        if not self._tron_service.is_valid_address(address):
            logger.warning(f"Invalid TRON address provided: {address}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid TRON address: {address}",
            )

        try:
            wallet_info = await self._tron_service.get_wallet_info(address)

            db_record = await self._wallet_request_repository.create(
                session=session,
                data={
                    "address": address,
                    "network": network,
                    "balance": wallet_info.balance,
                    "bandwidth": wallet_info.bandwidth,
                    "energy": wallet_info.energy,
                },
            )

            logger.info(
                f"Successfully saved wallet info for {address} with ID: {db_record.id}"
            )

            return WalletRequestResponse.model_validate(db_record)
        except TronClientError as e:
            logger.error(f"TRON client error for address {address}: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to get wallet information from TRON network: {str(e)}",
            )
        except Exception as e:
            logger.error(f"Unexpected error getting wallet info for {address}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while processing wallet request",
            )

    async def get_wallet_requests_paginated(
        self, session: AsyncSession, pagination: PaginationParams
    ) -> PaginatedWalletRequestResponse:
        """
        Получает список запросов кошельков с пагинацией

        Args:
            session: Сессия базы данных
            pagination: Параметры пагинации

        Returns:
            PaginatedWalletRequestResponse: Список запросов с пагинацией

        Raises:
            HTTPException: При ошибках базы данных
        """
        try:
            logger.info(
                f"Getting paginated wallet requests: page={pagination.page}, limit={pagination.limit}"
            )

            items = await self._wallet_request_repository.get_all(
                session=session, offset=pagination.offset, limit=pagination.limit
            )
            total = await self._wallet_request_repository.get_count(session=session)

            wallet_responses = [
                WalletRequestResponse.model_validate(item) for item in items
            ]

            response = PaginatedWalletRequestResponse.create(
                items=wallet_responses,
                total=total,
                page=pagination.page,
                limit=pagination.limit,
            )

            logger.info(
                f"Successfully retrieved {len(items)} wallet requests from total {total}"
            )

            return response
        except Exception as e:
            logger.error(f"Error getting paginated wallet requests: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error while retrieving wallet requests",
            )
