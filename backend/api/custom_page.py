from typing import TypeVar
from fastapi_pagination import Page
from fastapi_pagination.bases import AbstractParams, RawParams
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi import Query
from pydantic import BaseModel

# T = TypeVar("T")
#
# CustomPage = CustomizedPage[
#     Page[T],
#     UseParamsFields(size=Query(le=10000))
# ]

class CustomParams(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(50, ge=1, le=10000, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size if self.size is not None else None,
            offset=self.size * (self.page - 1) if self.page is not None and self.size is not None else None,
        )