from decimal import Decimal
from http import HTTPStatus
from unittest.mock import patch

import pytest

from enums.network import NetworkEnum
from schemas import WalletInfo
from tests.factories import WalletFactory
from tests.test_api.base import BaseTestCase


class TestGetWalletInfo(BaseTestCase):
    url = "/wallet"
    network = NetworkEnum.TRON
    address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    balance = Decimal("100.123456")
    bandwidth = 1000
    energy = 2000

    @pytest.fixture
    def _mock_explorer(self):
        with (
            patch(
                "explorers.tron.TronExplorer.get_wallet_info"
            ) as mock_get_wallet_info,
            patch(
                "explorers.tron.TronExplorer.check_is_valid_address"
            ) as mock_check_is_valid_address,
        ):
            mock_get_wallet_info.return_value = WalletInfo(
                network=self.network,
                address=self.address,
                balance=self.balance,
                bandwidth=self.bandwidth,
                energy=self.energy,
            )
            mock_check_is_valid_address.return_value = None
            yield

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("_mock_explorer")
    async def test_ok(self) -> None:
        response = await self.client.post(
            url=self.url,
            params={"network": self.network.value},
            json={"address": self.address},
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["network"] == self.network.value
        assert data["address"] == self.address
        assert Decimal(data["balance"]) == self.balance
        assert data["bandwidth"] == self.bandwidth
        assert data["energy"] == self.energy


class TestGetWalletHistory(BaseTestCase):
    url = "/wallet/history"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        limit = 10
        items_count = 15
        [
            await WalletFactory.create_async(session=self.session)
            for _ in range(items_count)
        ]

        response = await self.client.get(url=self.url, params={"limit": limit})

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["results"]) == limit
        assert data["count"] == items_count
        assert data["page"] == 1
        assert data["limit"] == limit
        assert data["pages"] == 2
        assert data["next"] == 2
        assert data["previous"] is None
