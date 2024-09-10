from typing import Annotated
from fastapi import APIRouter, Body, Path, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from .mapper import map_lds_link_to_link, map_link_to_lds_link
from ..db import engine
from ..schemas import Error, Link, UpdateLink
from database import lds

router = APIRouter(prefix="/link", tags=["link"])


@router.get('', response_model=list[Link] | Error)
async def list_links(filter: Annotated[str | None, Query()] = None):
    try:
        statement = select(lds.Link)
        with Session(engine) as session:
            links = session.execute(statement).all()
        links_out = [map_lds_link_to_link(lds_link[0]) for lds_link in links]
        return links_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_links(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=Link | Error)
async def create_event_def(link: Annotated[Link, Body()]):
    try:
        lds_link = map_link_to_lds_link(link)
        with Session(engine) as session:
            session.add(lds_link)
            session.commit()
            session.refresh(lds_link)
        link = map_lds_link_to_link(lds_link)
        return link
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Link with id = ' + str(link.id) + ' already exists')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_link(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{link_id}', response_model=None | Error)
async def delete_link_by_id(link_id: Annotated[int, Path()]):
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
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when deleting link with id = ' + str(link_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_link_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{link_id}', response_model=Link | Error)
async def get_link_by_id(link_id: Annotated[int, Path()]):
    try:
        with Session(engine) as session:
            link = session.get(lds.Link, link_id)
        if not link:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No link with id = ' + str(link_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return map_lds_link_to_link(link)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_link_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{link_id}', response_model=Link | Error)
async def update_event_def(link_id: Annotated[str, Path()], updated_link: Annotated[UpdateLink, Body()]):
    try:
        with Session(engine) as session:
            link = session.get(lds.EventDef, link_id)
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
