from abc import ABC, abstractmethod

from schemas.wallet import WalletInfo


class BaseExplorer(ABC):
    @abstractmethod
    async def get_wallet_info(self, address: str) -> WalletInfo:
        """Get wallet info from explorer

        Args:
            address: The address of the wallet

        Returns:
            The wallet info

        """
        pass

    @abstractmethod
    async def is_valid_address(self, address: str) -> bool:
        """Check if the address is valid

        Args:
            address: The address of the wallet

        Returns:
            True if the address is valid, False otherwise

        """
        pass
