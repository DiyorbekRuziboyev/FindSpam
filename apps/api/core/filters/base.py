from datetime import datetime
from enum import StrEnum
from typing import Any

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy import Select, asc, desc


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class BaseFilter(BaseModel):
    sort_by: str | None = None
    sort_order: SortOrder = SortOrder.DESC
    created_after: datetime | None = None
    created_before: datetime | None = None

    model_config = {"arbitrary_types_allowed": True}

    def apply_sorting(self, query: Select[Any], model: Any) -> Select[Any]:
        if self.sort_by and hasattr(model, self.sort_by):
            column = getattr(model, self.sort_by)
            query = query.order_by(asc(column) if self.sort_order == SortOrder.ASC else desc(column))
        elif hasattr(model, "created_at"):
            query = query.order_by(desc(model.created_at))
        return query

    def apply_date_range(self, query: Select[Any], model: Any) -> Select[Any]:
        if self.created_after and hasattr(model, "created_at"):
            query = query.where(model.created_at >= self.created_after)
        if self.created_before and hasattr(model, "created_at"):
            query = query.where(model.created_at <= self.created_before)
        return query
