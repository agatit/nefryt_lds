from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine
from sqlalchemy.exc import IntegrityError
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import strip_strings, get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/simulation", tags=["simulation"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Simulation] | api.Error)
async def list_simulations(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                           _: Annotated[None, Depends(use_custom_page)],
                           odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.Simulation).order_by(lds.Simulation.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_simulation) for lds_simulation in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_simulations(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Simulation | api.Error)
async def create_simulation(simulation: Annotated[api.SimulationCreate, Body()],
                            engine: Annotated[Engine, Depends(get_engine)]):
    try:
        simulation = lds.Simulation(**simulation.model_dump())
        with Session(engine) as session:
            session.add(simulation)
            session.commit()
            session.refresh(simulation)
        content = strip_strings(simulation).model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating simulation')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_simulation(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{simulation_id}', response_model=api.Information | api.Error)
async def delete_simulation_by_id(simulation_id: Annotated[int, Path()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            simulation = session.get(lds.Simulation, simulation_id)
            if not simulation:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation with id = ' + str(simulation_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(simulation)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_simulation_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{simulation_id}', response_model=lds.Simulation | api.Error)
async def get_simulation_by_id(simulation_id: int, engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_simulation = session.get(lds.Simulation, simulation_id)
        if not lds_simulation:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return strip_strings(lds_simulation)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_simulation_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{simulation_id}', response_model=lds.Simulation | api.Error)
async def update_simulation(simulation_id: Annotated[int, Path()],
                            updated_simulation: Annotated[api.SimulationUpdate, Body()],
                            engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            simulation = session.get(lds.Simulation, simulation_id)
            if not simulation:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation with id = ' + str(simulation_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_simulation_dict = updated_simulation.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_simulation_dict.items():
                setattr(simulation, k, v)
            session.commit()
            session.refresh(simulation)
        return strip_strings(simulation)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating simulation with id = ' + str(simulation_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_simulation(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
