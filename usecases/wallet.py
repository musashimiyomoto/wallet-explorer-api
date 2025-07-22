from sqlalchemy.ext.asyncio import AsyncSession

from explorers.base import BaseExplorer
from repositories import WalletRepository
from schemas import (
    PaginatedResponse,
    SortingAndPaginationParams,
    WalletInfo,
    WalletResponse,
)


class WalletUsecase:
    def __init__(self, explorer: BaseExplorer):
        self._wallet_repository = WalletRepository()
        self._explorer = explorer

    async def get_wallet_info(self, address: str) -> WalletInfo:
        """Get wallet info from explorer.

        Args:
            address: The address of the wallet.

        Returns:
            The wallet info.

        Raises:
            InvalidAddressException: If the address is invalid.

        """
        self._explorer.check_is_valid_address(address=address)
        return await self._explorer.get_wallet_info(address=address)

    async def save_wallet_info(
        self, session: AsyncSession, wallet_info: WalletInfo
    ) -> None:
        """Save wallet info to database.

        Args:
            session: The database session.
            wallet_info: The wallet info.

        """
        await self._wallet_repository.create(
            session=session, data=wallet_info.model_dump()
        )

    async def get_history(
        self, session: AsyncSession, data: SortingAndPaginationParams
    ) -> PaginatedResponse[WalletResponse]:
        """Get wallet history from database.

        Args:
            session: The database session.
            data: The sorting and pagination params.

        Returns:
            The wallet history.

        """
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
