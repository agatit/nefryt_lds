from math import ceil
from typing import TypeVar, Generic, Sequence, Optional, Any, AsyncGenerator
from fastapi_pagination import set_page
from fastapi_pagination.bases import AbstractParams, RawParams, AbstractPage
from fastapi import Query
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from pydantic import BaseModel


async def use_custom_page() -> AsyncGenerator[None, None]:
    with set_page(CustomPage):
        yield


class CustomParams(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(50, ge=1, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size if self.size is not None else None,
            offset=self.size * (self.page - 1) if self.page is not None and self.size is not None else None,
        )


T = TypeVar("T")


class CustomPage(AbstractPage[T], Generic[T]): # noqa
    items: Sequence[T]
    total: Optional[GreaterEqualZero]
    page: Optional[GreaterEqualOne]
    size: Optional[GreaterEqualOne]
    pages: Optional[GreaterEqualZero] = None

    __params_type__ = CustomParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: CustomParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any
    ):
        page = params.page if params.page is not None else 1
        size = params.size if params.size is not None else (total or None)

        if size in {0, None}:
            pages = 0
        elif total is not None:
            pages = ceil(total / size)
        else:
            pages = None

        return cls(
            total=total,
            items=items,
            page=page,
            size=size,
            pages=pages,
        )
