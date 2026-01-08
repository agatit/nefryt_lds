from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy import select, Engine, literal
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from api.routers.utils import get_user_token, map_lds_simulation_data_to_api_simulation_data
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/simulation", tags=["simulation_data"], dependencies=[Depends(get_user_token)])


@router.get('/{simulation_id}/data', response_model=CustomPage[api.SimulationData] | api.Error)
async def get_simulation_data(simulation_id: Annotated[int, Path()],
                              engine: Annotated[Engine, Depends(get_engine)],
                              params: Annotated[CustomParams, Depends()],
                              _: Annotated[None, Depends(use_custom_page)]):
    try:
        with Session(engine) as session:
            lds_simulation = session.get(lds.Simulation, simulation_id)
        if not lds_simulation:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        with Session(engine) as session:
            lds_simulation_param = session.get(lds.SimulationParam, (simulation_id, 'LENGTH'))
        if not lds_simulation_param:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                          message='No simulation param with id = \'LENGTH\' for simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        distances = [distance for distance in range(0, int(lds_simulation_param.Value), lds_simulation.ResolutionMeters)]
        statement = (select(lds.SimulationData)
                     .where(lds.SimulationData.SimulationID == literal(simulation_id)) # noqa
                     .order_by(lds.SimulationData.Distance))

        with Session(engine) as session:
            lds_simulation_data_rows = session.execute(statement).all()
        lds_simulation_data: list[lds.SimulationData] = [data[0] for data in lds_simulation_data_rows]

        if len(lds_simulation_data) == 0:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                          message='No simulation data for simulation with id = ' + str(simulation_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        simulation_data_out = map_lds_simulation_data_to_api_simulation_data(lds_simulation_data, distances)
        simulation_data_out.Data = simulation_data_out.Data[(params.page-1)*params.size: params.page*params.size]
        return CustomPage(items=[simulation_data_out], total=len(distances),
                          pages=len(distances)//params.size if len(distances)//params.size > 0 else 1,
                          page=params.page, size=params.size)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in list_simulation_params_by_simulation_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
