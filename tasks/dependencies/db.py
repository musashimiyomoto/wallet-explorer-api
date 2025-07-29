from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends

from db.sessions import async_session


async def get_session(
    request: Request = TaskiqDepends(),  # noqa: B008
) -> AsyncGenerator[AsyncSession, None]:
    """Get the session.

    Args:
        request: Request.

    Yields:
        The session.

    """
    async with async_session() as session:
        yield session
