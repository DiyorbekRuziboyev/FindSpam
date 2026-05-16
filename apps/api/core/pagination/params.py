import math
from dataclasses import dataclass

from fastapi import Query

from core.schemas.response import PaginationMeta

_MAX_PAGE_SIZE = 100
_DEFAULT_PAGE_SIZE = 20


@dataclass
class PaginationParams:
    page: int
    page_size: int

    @classmethod
    def as_dependency(
        cls,
        page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
        page_size: int = Query(
            default=_DEFAULT_PAGE_SIZE, ge=1, le=_MAX_PAGE_SIZE, description="Items per page"
        ),
    ) -> "PaginationParams":
        return cls(page=page, page_size=page_size)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

    def build_meta(self, total_items: int) -> PaginationMeta:
        total_pages = max(1, math.ceil(total_items / self.page_size))
        return PaginationMeta(
            page=self.page,
            page_size=self.page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=self.page < total_pages,
            has_prev=self.page > 1,
        )
