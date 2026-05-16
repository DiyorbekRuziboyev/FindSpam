from typing import Generic, TypeVar

from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class StandardResponse(BaseModel, Generic[DataT]):
    success: bool = True
    data: DataT
    message: str | None = None


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel, Generic[DataT]):
    success: bool = True
    data: list[DataT]
    meta: PaginationMeta


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: dict[str, object] = Field(
        default_factory=lambda: {"code": "UNKNOWN_ERROR", "message": "An error occurred"}
    )
