from typing import Annotated
from fastapi import APIRouter, Body, Path, Query
from sqlalchemy import select, delete, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from .mapper import map_event_def_to_lds_event_def, map_lds_event_def_to_event_def, map_lds_node_to_node, \
    map_node_to_lds_node
from ..db import engine
from ..schemas import Error, EventDef, Information, UpdateEventDef, Node, UpdateNode
from database import lds

router = APIRouter(prefix="/node", tags=["node"])


@router.get('', response_model=list[Node] | Error)
async def list_nodes(filter: Annotated[str | None, Query()] = None):
    try:
        statement = select(lds.Node)
        with Session(engine) as session:
            nodes = session.execute(statement).all()
        nodes_out = [map_lds_node_to_node(node[0]) for node in nodes]
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
        return map_lds_node_to_node(lds_node)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Node with id = ' + str(node.id) + ' already exists')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_node(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{node_id}', response_model=None | Error)
async def delete_node_by_id(node_id: Annotated[int, Path()]):
    try:
        with Session(engine) as session:
            node = session.get(lds.Node, node_id)
            if not node:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No node with id = ' + str(node_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            statement = delete(lds.Link).where(or_(lds.Link.BeginNodeID == node_id, lds.Link.EndNodeID == node.id))
            session.execute(statement)
            session.delete(node)
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
        with Session(engine) as session:
            node = session.get(lds.EventDef, node_id)
        if not node:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No node with id = ' + str(node_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return map_lds_node_to_node(node)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_node_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{node_id}', response_model=Node | Error)
async def update_node(node_id: Annotated[int, Path()], updated_node: Annotated[UpdateNode, Body()]):
    try:
        with Session(engine) as session:
            node = session.get(lds.Node, node_id)
            if not node:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No node with id = ' + str(node_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_node_dict = updated_node.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_node_dict.items():
                setattr(node, k, v)
            session.commit()
            session.refresh(node)
        return node
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating node with id = ' + str(node))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_node(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
