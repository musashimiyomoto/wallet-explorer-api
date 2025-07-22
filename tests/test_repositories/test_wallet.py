from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from enums.network import NetworkEnum
from repositories import WalletRepository
from tests.factories import WalletFactory


@pytest.fixture
def repository() -> WalletRepository:
    return WalletRepository()


class TestCreate:
    network = NetworkEnum.TRON
    address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    balance = Decimal("100.123456")
    bandwidth = 1000
    energy = 2000

    @pytest.mark.asyncio
    async def test_success(
        self, test_session: AsyncSession, repository: WalletRepository
    ) -> None:
        wallet_request = await repository.create(
            session=test_session,
            data={
                "network": self.network,
                "address": self.address,
                "balance": self.balance,
                "bandwidth": self.bandwidth,
                "energy": self.energy,
            },
        )

        assert wallet_request.id is not None
        assert wallet_request.network == self.network
        assert wallet_request.address == self.address
        assert wallet_request.balance == self.balance
        assert wallet_request.bandwidth == self.bandwidth
        assert wallet_request.energy == self.energy
        assert wallet_request.created_at is not None


class TestGetAll:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("offset", "limit", "expected_items_count"), [(0, 3, 3), (3, 3, 0)]
    )
    async def test_get_all(
        self,
        test_session: AsyncSession,
        repository: WalletRepository,
        offset: int,
        limit: int,
        expected_items_count: int,
    ) -> None:
        items_count = 3
        [
            await WalletFactory.create_async(session=test_session)
            for _ in range(items_count)
        ]

        items = await repository.get_all(
            session=test_session, offset=offset, limit=limit
        )

        assert len(items) == expected_items_count
