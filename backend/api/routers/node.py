from typing import Annotated
from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine, literal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import map_lds_node_and_editor_node_to_node_out, map_node_to_lds_node, map_node_to_editor_node, get_user_token
from ..custom_page import CustomParams, CustomPage, use_custom_page
from db import get_engine
from ..schemas import api
from database import lds, editor

router = APIRouter(prefix="/node", tags=["node"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[api.Node] | api.Error)
async def list_nodes(engine: Annotated[Engine, Depends(get_engine)],  params: Annotated[CustomParams, Depends()],
                     _: Annotated[None, Depends(use_custom_page)],
                     odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        lds_node = aliased(lds.Node)
        editor_node = aliased(editor.Node)
        statement = (select(lds_node, editor_node)
                     .outerjoin(editor_node, lds_node.ID == editor_node.ID) # noqa
                     .order_by(lds_node.ID))
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [map_lds_node_and_editor_node_to_node_out(lds_node, editor_node)
                      for lds_node, editor_node in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_nodes(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=api.Node | api.Error)
async def create_node(node: Annotated[api.NodeCreate, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        lds_node = map_node_to_lds_node(node)
        with Session(engine) as session:
            session.add(lds_node)
            session.commit()
            session.refresh(lds_node)
            editor_node = map_node_to_editor_node(lds_node.ID, node)
            if editor_node:
                session.add(editor_node)
                session.commit()
                session.refresh(editor_node)
            node = map_lds_node_and_editor_node_to_node_out(lds_node, editor_node)
            return JSONResponse(content=node.model_dump(by_alias=True), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating node')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_node(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{node_id}', response_model=None | api.Error)
async def delete_node_by_id(node_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        lds_node = aliased(lds.Node)
        editor_node = aliased(editor.Node)
        statement = (select(lds_node, editor_node)
                     .outerjoin(editor_node, lds_node.ID == editor_node.ID) # noqa
                     .where(lds_node.ID == literal(node_id)))
        with Session(engine) as session:
            node = session.execute(statement).all()
        if not node:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No node with id = ' + str(node_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_node, editor_node = node[0]
        session.delete(lds_node)
        if editor_node:
            session.delete(editor_node)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when deleting node with id = ' + str(node_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_node_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{node_id}', response_model=api.Node | api.Error)
async def get_node_by_id(node_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        lds_node = aliased(lds.Node)
        editor_node = aliased(editor.Node)
        statement = (select(lds_node, editor_node)
                     .outerjoin(editor_node, lds_node.ID == editor_node.ID)  # noqa
                     .where(lds_node.ID == literal(node_id)))
        with Session(engine) as session:
            node = session.execute(statement).all()
        if not node:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No node with id = ' + str(node_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_node, editor_node = node[0]
        return map_lds_node_and_editor_node_to_node_out(lds_node, editor_node)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_node_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{node_id}', response_model=api.Node | api.Error)
async def update_node(node_id: Annotated[int, Path()], updated_node: Annotated[api.NodeUpdate, Body()],
                      engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_node = aliased(lds.Node)
            editor_node = aliased(editor.Node)
            statement = (select(lds_node, editor_node)
                         .outerjoin(editor_node, lds_node.ID == editor_node.ID) # noqa
                         .where(lds_node.ID == literal(node_id)))
            node = session.execute(statement).all()
            if not node:
                error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No node with id = ' + str(node_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_node, editor_node = node[0]
            updated_node_dict = updated_node.model_dump(by_alias=True, exclude_unset=True)
            if 'EditorParams' in updated_node_dict.keys():
                editor_params = updated_node_dict.pop('EditorParams')
                for k, v in editor_params.items():
                    setattr(editor_node, k, v)
            for k, v in updated_node_dict.items():
                setattr(lds_node, k, v)
            session.commit()
            session.refresh(lds_node)
            session.refresh(editor_node)
            return map_lds_node_and_editor_node_to_node_out(lds_node, editor_node)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_node(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
