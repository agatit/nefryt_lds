from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine, literal, and_
from sqlalchemy.exc import IntegrityError
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import get_user_token, \
    map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out, \
    map_simulation_param_base_to_lds_simulation_param, strip_strings
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/simulation", tags=["simulation_param"], dependencies=[Depends(get_user_token)])


@router.get('/param/def', response_model=CustomPage[lds.SimulationParamDef] | api.Error)
async def list_simulation_param_defs(engine: Annotated[Engine, Depends(get_engine)],
                                     params: Annotated[CustomParams, Depends()],
                                     _: Annotated[None, Depends(use_custom_page)],
                                     odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.SimulationParamDef).order_by(lds.SimulationParamDef.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_simulation_param_def) for lds_simulation_param_def in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_simulation_param_defs(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.get('/{simulation_id}/param', response_model=CustomPage[api.SimulationParam] | api.Error)
async def list_simulation_params_by_simulation_id(simulation_id: Annotated[int, Path()],
                                                  engine: Annotated[Engine, Depends(get_engine)],
                                                  params: Annotated[CustomParams, Depends()],
                                                  _: Annotated[None, Depends(use_custom_page)],
                                                  odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(1).where(lds.Simulation.ID == literal(simulation_id))  # noqa
        with Session(engine) as session:
            simulation_exists = session.execute(statement).first()
        if not simulation_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.SimulationParam, lds.SimulationParamDef)
                     .select_from(lds.SimulationParam)
                     .join(lds.SimulationParamDef,
                           and_(lds.SimulationParam.SimulationParamDefID == lds.SimulationParamDef.ID,
                                lds.SimulationParam.SimulationDefID == lds.SimulationParamDef.SimulationDefID))
                     .join(lds.Simulation, and_(lds.Simulation.SimulationDefID == lds.SimulationParam.SimulationDefID,
                                                lds.Simulation.ID == lds.SimulationParam.SimulationID))
                     .where(lds.SimulationParam.SimulationID == literal(simulation_id)) # noqa
                     .order_by(lds.SimulationParamDef.ID))
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out(lds_simulation_param, lds_simulation_param_def, simulation_id)
            for lds_simulation_param, lds_simulation_param_def in page.items
        ]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in list_simulation_params_by_simulation_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{simulation_id}/param/all', response_model=CustomPage[api.SimulationParam] | api.Error)
async def list_required_simulation_params_by_simulation_id(simulation_id: Annotated[int, Path()],
                                                  engine: Annotated[Engine, Depends(get_engine)],
                                                  params: Annotated[CustomParams, Depends()],
                                                  _: Annotated[None, Depends(use_custom_page)],
                                                  odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(1).where(lds.Simulation.ID == literal(simulation_id))  # noqa
        with Session(engine) as session:
            simulation_exists = session.execute(statement).first()
        if not simulation_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (
            select(lds.SimulationParamDef, lds.SimulationParam, lds.Simulation)
            .join(lds.SimulationParamDef, lds.Simulation.SimulationDefID == lds.SimulationParamDef.SimulationDefID) # noqa
            .join(lds.SimulationParam,
                  and_(lds.SimulationParamDef.ID == lds.SimulationParam.SimulationParamDefID, lds.Simulation.ID == lds.SimulationParam.SimulationID), isouter=True)
            .where(lds.Simulation.ID == literal(simulation_id))
            .order_by(lds.SimulationParamDef.ID))

        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out(lds_simulation_param, lds_simulation_param_def, simulation_id)
            for lds_simulation_param_def, lds_simulation_param, _ in page.items
        ]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in list_required_simulation_params_by_simulation_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{simulation_id}/param/{simulation_param_def_id}', response_model=api.SimulationParam | api.Error)
async def get_simulation_param_by_id(simulation_id: Annotated[int, Path()],
                                                          simulation_param_def_id: Annotated[str, Path()],
                                                          engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Simulation.ID == literal(simulation_id))  # noqa
        with Session(engine) as session:
            simulation_exists = session.execute(statement).first()
        if not simulation_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.SimulationParam, lds.SimulationParamDef)
                     .select_from(lds.SimulationParam)
                     .join(lds.SimulationParamDef,
                           and_(lds.SimulationParam.SimulationParamDefID == lds.SimulationParamDef.ID,
                                lds.SimulationParam.SimulationDefID == lds.SimulationParamDef.SimulationDefID))
                     .join(lds.Simulation, and_(lds.Simulation.SimulationDefID == lds.SimulationParam.SimulationDefID,
                                                lds.Simulation.ID == lds.SimulationParam.SimulationID))
                     .where(lds.SimulationParam.SimulationID == literal(simulation_id)) # noqa
                     .where(lds.SimulationParamDef.ID == literal(simulation_param_def_id)))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                          message='No simulation param for simulation with id = ' + str(simulation_id)
                                  + ' and simulation param def with id = ' + simulation_param_def_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_simulation_param, lds_simulation_param_def = results[0]
        return map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out(lds_simulation_param,
                                                                                             lds_simulation_param_def, simulation_id)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_simulation_param_by_simulation_param_def_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{simulation_id}/param/{simulation_param_def_id}', response_model=api.SimulationParam | api.Error)
async def update_simulation_param(simulation_id: Annotated[int, Path()],
                                  simulation_param_def_id: Annotated[str, Path()],
                                  updated_simulation_param_value: Annotated[str, Body()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Simulation.ID == literal(simulation_id))  # noqa
        with Session(engine) as session:
            simulation_exists = session.execute(statement).first()
        if not simulation_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.SimulationParam)
                     .where(lds.SimulationParam.SimulationParamDefID == literal(simulation_param_def_id)) # noqa
                     .where(lds.SimulationParam.SimulationID == literal(simulation_id)))
        with Session(engine) as session:
            lds_simulation_param = session.execute(statement).all()
            if not lds_simulation_param:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation param for simulation with id = ' + str(simulation_id)
                                      + ' and simulation param def with id = ' + simulation_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_simulation_param = lds_simulation_param[0][0]
            lds_simulation_param.Value = updated_simulation_param_value
            session.commit()
        return await get_simulation_param_by_id(simulation_id, simulation_param_def_id, engine)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when updating simulation')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in update_simulation_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{simulation_id}/param', response_model=api.SimulationParam | api.Error)
async def create_simulation_param(simulation_id: Annotated[int, Path()],
                                  simulation_param: Annotated[api.SimulationParamCreate, Body()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_simulation: lds.Simulation | None = session.get(lds.Simulation, simulation_id)
            if not lds_simulation:
                error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_simulation_param_def: lds.SimulationParamDef | None = session.get(lds.SimulationParamDef, (simulation_param.SimulationParamDefID, lds_simulation.SimulationDefID))
            if not lds_simulation_param_def:
                error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation param def with id = ' + simulation_param.SimulationParamDefID)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        lds_simulation_param = map_simulation_param_base_to_lds_simulation_param(simulation_param, lds_simulation)
        with Session(engine) as session:
            session.add(lds_simulation_param)
            session.commit()
            session.refresh(lds_simulation_param)
        simulation_param_out = (map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out
                   (lds_simulation_param, lds_simulation_param_def, simulation_id))

        return JSONResponse(content=simulation_param_out.model_dump(), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating simulation param')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in create_simulation_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{simulation_id}/param/{simulation_param_def_id}', response_model=api.Information | api.Error)
async def delete_simulation_param_by_id(simulation_id: Annotated[int, Path()],
                                  simulation_param_def_id: Annotated[str, Path()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_simulation = session.get(lds.Simulation, simulation_id)
        if not lds_simulation:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        with Session(engine) as session:
            lds_simulation_param = session.get(lds.SimulationParam, (simulation_id, simulation_param_def_id))
            if not lds_simulation_param:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation param for simulation with id = ' + str(simulation_id)
                                      + ' and simulation param def with id = ' + simulation_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(lds_simulation_param)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_simulation_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
