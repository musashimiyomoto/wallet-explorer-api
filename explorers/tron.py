import logging
from decimal import Decimal

from tronpy import AsyncTron
from tronpy.exceptions import ApiError

from explorers.base import BaseExplorer
from schemas.wallet import WalletInfo

logger = logging.getLogger(__name__)


class TronExplorer(BaseExplorer):
    def __init__(self):
        self._client = AsyncTron()

    async def get_wallet_info(self, address: str) -> WalletInfo:
        try:
            account_info = await self._client.get_account(address)

            balance_sun = account_info.get("balance", 0)
            balance_trx = Decimal(balance_sun) / Decimal(1_000_000)

            account_resource = await self._client.get_account_resource(address)

            bandwidth = account_resource.get("freeNetUsed", 0)
            bandwidth_limit = account_resource.get("freeNetLimit", 0)
            available_bandwidth = max(0, bandwidth_limit - bandwidth)

            energy_used = account_resource.get("EnergyUsed", 0)
            energy_limit = account_resource.get("EnergyLimit", 0)
            available_energy = max(0, energy_limit - energy_used)

            logger.info(
                f"Retrieved wallet info for {address}: "
                f"balance={balance_trx} TRX, "
                f"bandwidth={available_bandwidth}, "
                f"energy={available_energy}"
            )

            return WalletInfo(
                balance=balance_trx,
                bandwidth=available_bandwidth,
                energy=available_energy,
            )
        except ApiError as e:
            logger.error(f"TRON API error for address {address}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting wallet info for {address}: {e}")
            raise

    async def is_valid_address(self, address: str) -> bool:
        return await self._client.is_address(address)
