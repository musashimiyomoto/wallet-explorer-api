from abc import ABC, abstractmethod

from schemas.wallet import WalletInfo


class BaseExplorer(ABC):
    @abstractmethod
    async def get_wallet_info(self, address: str) -> WalletInfo:
        """Get wallet info from explorer.

        Args:
            address: The address of the wallet.

        Returns:
            The wallet info.

        """
        pass

    @abstractmethod
    def check_is_valid_address(self, address: str) -> None:
        """Check if the address is valid.

        Args:
            address: The address to check.

        Raises:
            InvalidAddressException: If the address is invalid.

        """
        pass
