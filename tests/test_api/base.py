import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


class BaseTestCase:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session: AsyncSession, test_client: AsyncClient) -> None:
        self.session = test_session
        self.client = test_client
