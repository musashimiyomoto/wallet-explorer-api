from typing import Any, Generic, Type, TypeVar

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from enums.sort import SortDirectionEnum

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model]):
        self.model = model

    async def create(self, session: AsyncSession, data: dict[str, Any]) -> Model:
        """Create a new model instance.

        Args:
            session: The async session.
            data: The data to create the model instance.

        Returns:
            The created model instance.

        """
        instance = self.model(**data)

        session.add(instance=instance)
        await session.commit()
        await session.refresh(instance)

        return instance

    async def get_all(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 10,
        order_by: str = "created_at",
        order_direction: SortDirectionEnum = SortDirectionEnum.DESC,
        **filters,
    ) -> list[Model]:
        """Get all model instances with pagination and sorting.

        Args:
            session: The async session.
            offset: The offset of the first item to return.
            limit: The maximum number of items to return.
            order_by: The field to sort by.
            order_direction: The direction to sort by.
            **filters: The filters to apply to the query.

        Returns:
            The list of model instances.

        """
        result = await session.execute(
            statement=(
                select(self.model)
                .filter_by(**filters)
                .order_by(
                    desc(getattr(self.model, order_by))
                    if order_direction == SortDirectionEnum.DESC
                    else asc(getattr(self.model, order_by))
                )
                .offset(offset)
                .limit(limit)
            )
        )
        return result.scalars().all()

    async def get_by(self, session: AsyncSession, **filters) -> Model | None:
        """Get a model instance by filters.

        Args:
            session: The async session.
            **filters: The filters to apply to the query.

        Returns:
            The model instance.

        """
        result = await session.execute(
            statement=select(self.model).filter_by(**filters)
        )
        return result.scalar_one_or_none()

    async def update_by(
        self, session: AsyncSession, data: dict[str, Any], **filters
    ) -> Model | None:
        """Update a model instance by filters.

        Args:
            session: The async session.
            data: The data to update the model instance.
            **filters: The filters to apply to the query.

        Returns:
            The updated model instance.

        """
        instance = await self.get_by(session=session, **filters)

        if instance:
            for key, value in data.items():
                setattr(instance, key, value)

            await session.commit()
            await session.refresh(instance=instance)

        return instance

    async def delete_by(self, session: AsyncSession, **filters) -> bool:
        """Delete a model instance by filters.

        Args:
            session: The async session.
            **filters: The filters to apply to the query.

        Returns:
            True if the model instance was deleted, False otherwise.

        """
        instance = await self.get_by(session=session, **filters)

        if instance:
            await session.delete(instance=instance)
            await session.commit()

            return True

        return False

    async def get_count(self, session: AsyncSession, **filters) -> int:
        """Get the count of model instances by filters.

        Args:
            session: The async session.
            **filters: The filters to apply to the query.

        Returns:
            The count of model instances.

        """
        result = await session.execute(
            statement=select(func.count(self.model.id)).filter_by(**filters)
        )
        return result.scalar()
