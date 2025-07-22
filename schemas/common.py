import math
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, computed_field

from enums.sort import SortDirectionEnum

ResponseT = TypeVar("ResponseT")


class SortingParams(BaseModel):
    sort_by: str | None = Field(
        default=None,
        description="Sorting field",
    )
    sort_direction: SortDirectionEnum | None = Field(
        default=None,
        description="Sorting direction",
    )


class PaginationParams(BaseModel):
    page: int = Field(default=1, description="Page number", ge=1)
    limit: int = Field(default=10, description="Items per page", ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class SortingAndPaginationParams(SortingParams, PaginationParams):
    pass


class PaginatedResponse(BaseModel, Generic[ResponseT]):
    count: int = Field(description="Total number of items", ge=0)
    limit: int = Field(description="Number of items per page", gt=0)
    page: int = Field(description="Current page", ge=0)
    results: list[ResponseT] = Field(description="List of items")

    @computed_field(description="Total number of pages")
    @property
    def pages(self) -> int:
        return int(math.ceil(self.count / self.limit))

    @computed_field(description="Next page")
    @property
    def next(self) -> int | None:
        return self.page + 1 if self.page < self.pages else None

    @computed_field(description="Previous page")
    @property
    def previous(self) -> int | None:
        return self.page - 1 if self.page > 1 else None
