from typing import Annotated
from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from .security import get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import Error, UpdateLink, LinkBase
from database import lds

router = APIRouter(prefix="/link", tags=["link"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Link] | Error)
async def list_links(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                     _: Annotated[None, Depends(use_custom_page)], filter: Annotated[str | None, Query()] = None):
    try:
        statement = select(lds.Link).order_by(lds.Link.ID) # noqa
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        return page
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_links(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Link | Error)
async def create_link(link: Annotated[LinkBase, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        link = lds.Link(**link.model_dump())
        with Session(engine) as session:
            session.add(link)
            session.commit()
            session.refresh(link)
        content = link.model_dump(by_alias=True)
        return JSONResponse(content=jsonable_encoder(content), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating link')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_link(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{link_id}', response_model=None | Error)
async def delete_link_by_id(link_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            link = session.get(lds.Link, link_id)
            if not link:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No link with id = ' + str(link_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(link)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_link_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{link_id}', response_model=lds.Link | Error)
async def get_link_by_id(link_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            link = session.get(lds.Link, link_id)
        if not link:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No link with id = ' + str(link_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return link
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_link_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{link_id}', response_model=lds.Link | Error)
async def update_link(link_id: Annotated[int, Path()], updated_link: Annotated[UpdateLink, Body()],
                      engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            link = session.get(lds.Link, link_id)
            if not link:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No link with id = ' + str(link_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_link_dict = updated_link.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_link_dict.items():
                setattr(link, k, v)
            session.commit()
            session.refresh(link)
        return link
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating link with id = ' + str(link_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_link(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
