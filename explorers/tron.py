from decimal import Decimal

from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from enums.network import NetworkEnum
from exceptions.explorers import InvalidAddressException
from explorers.base import BaseExplorer
from schemas.wallet import WalletInfo
from settings.explorer import explorer_settings


class TronExplorer(BaseExplorer):
    def __init__(self):
        self._client = AsyncTron(
            provider=AsyncHTTPProvider(api_key=explorer_settings.tron_api_key)
        )

    async def get_wallet_info(self, address: str) -> WalletInfo:
        account_info = await self._client.get_account(addr=address)
        account_resource = await self._client.get_account_resource(addr=address)

        return WalletInfo(
            network=NetworkEnum.TRON,
            address=address,
            balance=Decimal(account_info.get("balance", "0.0")) / Decimal(1_000_000),
            bandwidth=max(
                0,
                account_resource.get("freeNetLimit", 0)
                - account_resource.get("freeNetUsed", 0),
            ),
            energy=max(
                0,
                account_resource.get("EnergyLimit", 0)
                - account_resource.get("EnergyUsed", 0),
            ),
        )

    def check_is_valid_address(self, address: str) -> None:
        try:
            if not self._client.is_address(value=address):
                raise InvalidAddressException()
        except ValueError:
            raise InvalidAddressException()
