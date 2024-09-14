from typing import Annotated
from fastapi import APIRouter, Body, Path, Query
from sqlalchemy import select, delete, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased
from starlette import status
from starlette.responses import JSONResponse, Response
from .mapper import map_lds_node_and_editor_node_to_node, map_node_to_lds_node, map_node_to_editor_node
from ..db import engine
from ..schemas import Error, Node, UpdateNode
from database import lds, editor

router = APIRouter(prefix="/node", tags=["node"])


@router.get('', response_model=list[Node] | Error)
async def list_nodes(filter: Annotated[str | None, Query()] = None):
    try:
        lds_node = aliased(lds.Node)
        editor_node = aliased(editor.Node)
        statement = (select(lds_node, editor_node)
                     .outerjoin(editor_node, lds_node.ID == editor_node.ID)) # noqa
        with Session(engine) as session:
            nodes = session.execute(statement).all()
        nodes_out = [map_lds_node_and_editor_node_to_node(lds_node, editor_node) for lds_node, editor_node in nodes]
        return nodes_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_nodes(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=Node | Error)
async def create_node(node: Annotated[Node, Body()]):
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
            node = map_lds_node_and_editor_node_to_node(lds_node, editor_node)
            return JSONResponse(content=node.model_dump(by_alias=True), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating node')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_node(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{node_id}', response_model=None | Error)
async def delete_node_by_id(node_id: Annotated[int, Path()]):
    try:
        lds_node = aliased(lds.Node)
        editor_node = aliased(editor.Node)
        statement = (select(lds_node, editor_node)
                     .outerjoin(editor_node, lds_node.ID == editor_node.ID)  # noqa
                     .where(lds_node.ID == node_id))
        with Session(engine) as session:
            node = session.execute(statement).all()
        if not node:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No node with id = ' + str(node_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_node, editor_node = node[0]
        session.delete(lds_node)
        if editor_node:
            session.delete(editor_node)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when deleting node with id = ' + str(node))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_node_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{node_id}', response_model=Node | Error)
async def get_node_by_id(node_id: Annotated[int, Path()]):
    try:
        lds_node = aliased(lds.Node)
        editor_node = aliased(editor.Node)
        statement = (select(lds_node, editor_node)
                     .outerjoin(editor_node, lds_node.ID == editor_node.ID) # noqa
                     .where(lds_node.ID == node_id))
        with Session(engine) as session:
            node = session.execute(statement).all()
        if not node:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No node with id = ' + str(node_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_node, editor_node = node[0]
        return map_lds_node_and_editor_node_to_node(lds_node, editor_node)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_node_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{node_id}', response_model=Node | Error)
async def update_node(node_id: Annotated[int, Path()], updated_node: Annotated[UpdateNode, Body()]):
    try:
        with Session(engine) as session:
            lds_node = aliased(lds.Node)
            editor_node = aliased(editor.Node)
            statement = (select(lds_node, editor_node)
                         .outerjoin(editor_node, lds_node.ID == editor_node.ID)  # noqa
                         .where(lds_node.ID == node_id))
            node = session.execute(statement).all()
            if not node:
                error = Error(code=status.HTTP_404_NOT_FOUND, message='No node with id = ' + str(node_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_node, editor_node = node[0]
            updated_node_dict = updated_node.model_dump(by_alias=True, exclude_unset=True)
            if 'EditorParams' in updated_node_dict.keys():
                editor_params = updated_node_dict.pop('EditorParams')
                for k, v in editor_params.items():
                    setattr(editor_node, k, v)
            if 'TrendID' in updated_node_dict.keys():
                updated_node_dict.pop('TrendID')
            for k, v in updated_node_dict.items():
                setattr(lds_node, k, v)
            session.commit()
            session.refresh(lds_node)
            session.refresh(editor_node)
            return map_lds_node_and_editor_node_to_node(lds_node, editor_node)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating node with id = ' + str(node))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_node(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
