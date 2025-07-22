from decimal import Decimal

import pytest

from enums.network import NetworkEnum
from repositories.wallet import WalletRepository
from tests.factories import WalletFactory


class TestWalletRequestRepository:
    """Тесты для репозитория WalletRequest"""

    @pytest.fixture
    def repository(self):
        return WalletRequestRepository()

    async def test_create_wallet_request(self, test_session, repository):
        """Тест создания новой записи кошелька"""
        data = {
            "network": NetworkEnum.TRON,
            "address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
            "balance": Decimal("100.123456"),
            "bandwidth": 1000,
            "energy": 2000,
        }

        # Создаем запись
        wallet_request = await repository.create(test_session, data)

        # Проверяем что запись создалась корректно
        assert wallet_request.id is not None
        assert wallet_request.network == NetworkEnum.TRON
        assert wallet_request.address == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        assert wallet_request.balance == Decimal("100.123456")
        assert wallet_request.bandwidth == 1000
        assert wallet_request.energy == 2000
        assert wallet_request.created_at is not None

    async def test_get_by_address_and_network(self, test_session, repository):
        """Тест поиска записи по адресу и сети"""
        # Создаем тестовую запись
        wallet_request = await WalletRequestFactory.create_async(test_session)

        # Ищем по адресу и сети
        found_request = await repository.get_by_address_and_network(
            test_session, address=wallet_request.address, network=wallet_request.network
        )

        # Проверяем что нашли правильную запись
        assert found_request is not None
        assert found_request.id == wallet_request.id
        assert found_request.address == wallet_request.address
        assert found_request.network == wallet_request.network

    async def test_get_by_address_and_network_not_found(self, test_session, repository):
        """Тест поиска несуществующей записи"""
        result = await repository.get_by_address_and_network(
            test_session,
            address="TNotExistentAddress123456789012345678",
            network=NetworkEnum.TRON,
        )

        assert result is None

    async def test_create_or_update_new_record(self, test_session, repository):
        """Тест создания новой записи через create_or_update"""
        address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        network = NetworkEnum.TRON
        balance = Decimal("150.5")
        bandwidth = 3000
        energy = 4000

        # Создаем новую запись
        wallet_request = await repository.create_or_update(
            test_session,
            address=address,
            network=network,
            balance=balance,
            bandwidth=bandwidth,
            energy=energy,
        )

        # Проверяем что запись создалась
        assert wallet_request.id is not None
        assert wallet_request.address == address
        assert wallet_request.network == network
        assert wallet_request.balance == balance
        assert wallet_request.bandwidth == bandwidth
        assert wallet_request.energy == energy

    async def test_create_or_update_existing_record(self, test_session, repository):
        """Тест обновления существующей записи через create_or_update"""
        # Создаем исходную запись
        original_request = await WalletRequestFactory.create_async(test_session)
        original_id = original_request.id

        # Обновляем запись с новыми данными
        new_balance = Decimal("999.888")
        new_bandwidth = 9999
        new_energy = 8888

        updated_request = await repository.create_or_update(
            test_session,
            address=original_request.address,
            network=original_request.network,
            balance=new_balance,
            bandwidth=new_bandwidth,
            energy=new_energy,
        )

        # Проверяем что ID не изменился, но данные обновились
        assert updated_request.id == original_id
        assert updated_request.address == original_request.address
        assert updated_request.network == original_request.network
        assert updated_request.balance == new_balance
        assert updated_request.bandwidth == new_bandwidth
        assert updated_request.energy == new_energy

    async def test_get_paginated_empty(self, test_session, repository):
        """Тест пагинации с пустой БД"""
        items, total = await repository.get_paginated(test_session, offset=0, limit=10)

        assert items == []
        assert total == 0

    async def test_get_paginated_with_data(self, test_session, repository):
        """Тест пагинации с данными"""
        # Создаем 5 тестовых записей
        wallet_requests = await WalletRequestFactory.create_batch_async(test_session, 5)

        # Получаем первую страницу (3 записи)
        items, total = await repository.get_paginated(test_session, offset=0, limit=3)

        assert len(items) == 3
        assert total == 5

        # Проверяем что записи отсортированы по created_at по убыванию
        for i in range(len(items) - 1):
            assert items[i].created_at >= items[i + 1].created_at

    async def test_get_paginated_second_page(self, test_session, repository):
        """Тест получения второй страницы"""
        # Создаем 5 тестовых записей
        await WalletRequestFactory.create_batch_async(test_session, 5)

        # Получаем вторую страницу (offset=3, limit=3)
        items, total = await repository.get_paginated(test_session, offset=3, limit=3)

        assert len(items) == 2  # Остается только 2 записи на второй странице
        assert total == 5
