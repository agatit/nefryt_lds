import traceback
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
from api.routers.utils import strip_strings, get_user_token, \
    map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out, \
    map_simulation_param_base_to_lds_simulation_param
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import Error, SimulationDefBase, SimulationBase, Information, UpdateSimulation, SimulationParamOut, \
    UpdateSimulationParam, SimulationParamIn

# TODO: uzupełnić openapi
# TODO: alembic
# TODO: getter simulation data
router = APIRouter(prefix="/simulation", tags=["simulation"], dependencies=[Depends(get_user_token)])


@router.get('/defs', response_model=CustomPage[SimulationDefBase] | Error)
async def list_simulation_defs(engine: Annotated[Engine, Depends(get_engine)],
                               params: Annotated[CustomParams, Depends()],
                               _: Annotated[None, Depends(use_custom_page)],
                               odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.SimulationDef).order_by(lds.SimulationDef.ID)  # noqa
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_simulation_def) for lds_simulation_def in page.items]
        return page
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in list_simulation_defs(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('', response_model=CustomPage[lds.Simulation] | Error)
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
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_simulations(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Simulation | Error)
async def create_simulation(simulation: Annotated[SimulationBase, Body()],
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
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating simulation')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_simulation(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{simulation_id}', response_model=Information | Error)
async def delete_simulation_by_id(simulation_id: Annotated[int, Path()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            simulation = session.get(lds.Simulation, simulation_id)
            if not simulation:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation with id = ' + str(simulation_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(simulation)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_simulation_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{simulation_id}', response_model=lds.Simulation | Error)
async def get_simulation_by_id(simulation_id: int, engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_simulation = session.get(lds.Simulation, simulation_id)
        if not lds_simulation:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return strip_strings(lds_simulation)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_simulation_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{simulation_id}', response_model=lds.Simulation | Error)
async def update_simulation(simulation_id: Annotated[int, Path()],
                            updated_simulation: Annotated[UpdateSimulation, Body()],
                            engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            simulation = session.get(lds.Simulation, simulation_id)
            if not simulation:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation with id = ' + str(simulation_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_simulation_dict = updated_simulation.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_simulation_dict.items():
                setattr(simulation, k, v)
            session.commit()
            session.refresh(simulation)
        return strip_strings(simulation)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating simulation with id = ' + str(simulation_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_simulation(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{simulation_id}/param', response_model=CustomPage[SimulationParamOut] | Error)
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
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
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
            map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out(lds_simulation_param,
                                                                                          lds_simulation_param_def)
            for lds_simulation_param, lds_simulation_param_def in page.items
        ]
        return page
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in list_simulation_params_by_simulation_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{simulation_id}/param/{simulation_param_def_id}', response_model=SimulationParamOut | Error)
async def get_simulation_param_by_simulation_param_def_id(simulation_id: Annotated[int, Path()],
                                                          simulation_param_def_id: Annotated[str, Path()],
                                                          engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Simulation.ID == literal(simulation_id))  # noqa
        with Session(engine) as session:
            simulation_exists = session.execute(statement).first()
        if not simulation_exists:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
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
            error = Error(code=status.HTTP_404_NOT_FOUND,
                          message='No simulation param for simulation with id = ' + str(simulation_id)
                                  + ' and simulation param def with id = ' + simulation_param_def_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_simulation_param, lds_simulation_param_def = results[0]
        return map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out(lds_simulation_param,
                                                                                             lds_simulation_param_def)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_simulation_param_by_simulation_param_def_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{simulation_id}/param/{simulation_param_def_id}', response_model=SimulationParamOut | Error)
async def update_simulation_param(simulation_id: Annotated[int, Path()],
                                  simulation_param_def_id: Annotated[str, Path()],
                                  updated_simulation_param: Annotated[UpdateSimulationParam, Body()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Simulation.ID == literal(simulation_id))  # noqa
        with Session(engine) as session:
            simulation_exists = session.execute(statement).first()
        if not simulation_exists:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.SimulationParam)
                     .where(lds.SimulationParam.SimulationParamDefID == literal(simulation_param_def_id)) # noqa
                     .where(lds.SimulationParam.SimulationID == literal(simulation_id)))
        with Session(engine) as session:
            lds_simulation_param = session.execute(statement).all()
            if not lds_simulation_param:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation param for simulation with id = ' + str(simulation_id)
                                      + ' and simulation param def with id = ' + simulation_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_simulation_param = lds_simulation_param[0][0]
            updated_simulation_dict = updated_simulation_param.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_simulation_dict.items():
                setattr(lds_simulation_param, k, v)
                if k == 'SimulationID':
                    new_simulation = await get_simulation_by_id(v, engine)
                    if type(new_simulation) == JSONResponse:
                        error = Error(code=status.HTTP_409_CONFLICT,
                                      message=f'No simulation with id = {v} given in update data')
                        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
                    lds_simulation_param.SimulationDefID = new_simulation.SimulationDefID
            session.commit()
            session.refresh(lds_simulation_param)
        return await get_simulation_param_by_simulation_param_def_id(lds_simulation_param.SimulationID,
                                                                     lds_simulation_param.SimulationParamDefID.strip(), engine)
    except IntegrityError:
        traceback.print_exc()
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when updating simulation')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in update_simulation_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{simulation_id}/param', response_model=SimulationParamOut | Error)
async def create_simulation_param(simulation_id: Annotated[int, Path()],
                                  simulation_param: Annotated[SimulationParamIn, Body()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_simulation: lds.Simulation | None = session.get(lds.Simulation, simulation_id)
            if not lds_simulation:
                error = Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_simulation_param_def: lds.SimulationParamDef | None = session.get(lds.SimulationParamDef, (simulation_param.SimulationParamDefID, lds_simulation.SimulationDefID))
            if not lds_simulation_param_def:
                error = Error(code=status.HTTP_404_NOT_FOUND, message='No simulation param def with id = ' + simulation_param.SimulationParamDefID)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        lds_simulation_param = map_simulation_param_base_to_lds_simulation_param(simulation_param, lds_simulation)
        with Session(engine) as session:
            session.add(lds_simulation_param)
            session.commit()
            session.refresh(lds_simulation_param)
        simulation_param_out = (map_lds_simulation_param_and_lds_simulation_param_def_to_simulation_param_out
                   (lds_simulation_param, lds_simulation_param_def))

        return JSONResponse(content=simulation_param_out.model_dump(), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating simulation param')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in create_simulation_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{simulation_id}/param/{simulation_param_def_id}', response_model=Information | Error)
async def delete_simulation_param_by_id(simulation_id: Annotated[int, Path()],
                                  simulation_param_def_id: Annotated[str, Path()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_simulation = session.get(lds.Simulation, simulation_id)
        if not lds_simulation:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        with Session(engine) as session:
            lds_simulation_param = session.get(lds.SimulationParam, (simulation_id, simulation_param_def_id))
            if not lds_simulation_param:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No simulation param for simulation with id = ' + str(simulation_id)
                                      + ' and simulation param def with id = ' + simulation_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(lds_simulation_param)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_simulation_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
