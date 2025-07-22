from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

from enums.network import NetworkEnum
from schemas.wallet import WalletInfo
from tests.factories import WalletFactory


class TestWalletAPI:
    @pytest.fixture
    def mock_wallet_info(self):
        return WalletInfo(balance=Decimal("123.456789"), bandwidth=5000, energy=10000)

    @pytest.fixture
    def valid_tron_address(self):
        return "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

    async def test_get_wallet_info_success(
        self, test_client, mock_wallet_info, valid_tron_address
    ):
        with (
            patch(
                "services.tron_client.tron_client.is_valid_address", return_value=True
            ),
            patch(
                "services.tron_client.tron_client.get_wallet_info",
                return_value=mock_wallet_info,
            ) as mock_get_info,
        ):

            response = await test_client.post(
                "/api/v1/wallet",
                json={"address": valid_tron_address, "network": "tron"},
            )

            assert response.status_code == 200
            data = response.json()

            # Проверяем структуру ответа
            assert "id" in data
            assert data["address"] == valid_tron_address
            assert data["network"] == "tron"
            assert data["balance"] == "123.456789"
            assert data["bandwidth"] == 5000
            assert data["energy"] == 10000
            assert "created_at" in data

            # Проверяем что TRON клиент был вызван
            mock_get_info.assert_called_once_with(valid_tron_address)

    async def test_get_wallet_info_invalid_address_format(self, test_client):
        """Тест с невалидным форматом TRON адреса"""
        response = await test_client.post(
            "/api/v1/wallet", json={"address": "invalid_address", "network": "tron"}
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    async def test_get_wallet_info_invalid_address_validation(
        self, test_client, valid_tron_address
    ):
        """Тест с адресом, не прошедшим валидацию в TRON сети"""
        with patch(
            "services.tron_client.tron_client.is_valid_address", return_value=False
        ):
            response = await test_client.post(
                "/api/v1/wallet",
                json={"address": valid_tron_address, "network": "tron"},
            )

            assert response.status_code == 400
            data = response.json()
            assert "Invalid TRON address" in data["detail"]

    async def test_get_wallet_info_tron_client_error(
        self, test_client, valid_tron_address
    ):
        """Тест обработки ошибки TRON клиента"""
        with (
            patch(
                "services.tron_client.tron_client.is_valid_address", return_value=True
            ),
            patch(
                "services.tron_client.tron_client.get_wallet_info",
                side_effect=TronClientError("Network error"),
            ),
        ):

            response = await test_client.post(
                "/api/v1/wallet",
                json={"address": valid_tron_address, "network": "tron"},
            )

            assert response.status_code == 502
            data = response.json()
            assert (
                "Failed to get wallet information from TRON network" in data["detail"]
            )

    async def test_get_wallet_info_missing_address(self, test_client):
        """Тест запроса без адреса"""
        response = await test_client.post("/api/v1/wallet", json={"network": "tron"})

        assert response.status_code == 422

    async def test_get_wallet_requests_empty(self, test_client):
        """Тест получения пустого списка запросов"""
        response = await test_client.get("/api/v1/wallet/requests")

        assert response.status_code == 200
        data = response.json()

        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["limit"] == 10
        assert data["pages"] == 1

    async def test_get_wallet_requests_with_data(self, test_client, test_session):
        """Тест получения списка запросов с данными"""
        # Создаем 3 тестовых записи
        wallet_requests = await WalletRequestFactory.create_batch_async(test_session, 3)

        response = await test_client.get("/api/v1/wallet/requests")

        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 3
        assert data["total"] == 3
        assert data["page"] == 1
        assert data["limit"] == 10
        assert data["pages"] == 1

        # Проверяем структуру первого элемента
        first_item = data["items"][0]
        assert "id" in first_item
        assert "address" in first_item
        assert "network" in first_item
        assert "balance" in first_item
        assert "bandwidth" in first_item
        assert "energy" in first_item
        assert "created_at" in first_item

    async def test_get_wallet_requests_pagination(self, test_client, test_session):
        """Тест пагинации списка запросов"""
        # Создаем 5 тестовых записей
        await WalletRequestFactory.create_batch_async(test_session, 5)

        # Получаем первую страницу с лимитом 2
        response = await test_client.get("/api/v1/wallet/requests?page=1&limit=2")

        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["limit"] == 2
        assert data["pages"] == 3

    async def test_get_wallet_requests_second_page(self, test_client, test_session):
        """Тест получения второй страницы"""
        # Создаем 5 тестовых записей
        await WalletRequestFactory.create_batch_async(test_session, 5)

        # Получаем вторую страницу с лимитом 2
        response = await test_client.get("/api/v1/wallet/requests?page=2&limit=2")

        assert response.status_code == 200
        data = response.json()

        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 2
        assert data["limit"] == 2
        assert data["pages"] == 3

    async def test_get_wallet_requests_invalid_page(self, test_client):
        """Тест с невалидным номером страницы"""
        response = await test_client.get("/api/v1/wallet/requests?page=0&limit=10")

        assert response.status_code == 422

    async def test_get_wallet_requests_invalid_limit(self, test_client):
        """Тест с невалидным лимитом"""
        response = await test_client.get("/api/v1/wallet/requests?page=1&limit=0")

        assert response.status_code == 422

    async def test_get_wallet_requests_limit_too_high(self, test_client):
        """Тест с лимитом выше максимального"""
        response = await test_client.get("/api/v1/wallet/requests?page=1&limit=101")

        assert response.status_code == 422

    async def test_wallet_creation_and_retrieval_integration(
        self, test_client, mock_wallet_info, valid_tron_address
    ):
        """Интеграционный тест: создание кошелька и его получение в списке"""
        # Создаем запись через POST эндпоинт
        with (
            patch(
                "services.tron_client.tron_client.is_valid_address", return_value=True
            ),
            patch(
                "services.tron_client.tron_client.get_wallet_info",
                return_value=mock_wallet_info,
            ),
        ):

            create_response = await test_client.post(
                "/api/v1/wallet",
                json={"address": valid_tron_address, "network": "tron"},
            )

            assert create_response.status_code == 200
            created_wallet = create_response.json()

            # Получаем список через GET эндпоинт
            list_response = await test_client.get("/api/v1/wallet/requests")

            assert list_response.status_code == 200
            data = list_response.json()

            # Проверяем что наша запись есть в списке
            assert data["total"] == 1
            assert len(data["items"]) == 1

            retrieved_wallet = data["items"][0]
            assert retrieved_wallet["id"] == created_wallet["id"]
            assert retrieved_wallet["address"] == valid_tron_address
