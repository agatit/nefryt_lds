import os
import sys
from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi_pagination import add_pagination
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import setup_engine
from db import get_engine
from .schemas import api
from .routers import (events_router, event_defs_router, trend_defs_router, trend_router, auth_router, link_router,
                      node_router, template_router, unit_router, trend_groups_router, trend_writer_router,
                      simulation_router, trend_params_router, trend_data_router, simulation_defs_router,
                      simulation_data_router, simulation_params_router, leak_detector_router, pipeline_router,
                      pipeline_params_router, method_router, method_def_router)

setup_engine()
app = FastAPI(title='Nefryt LDS API',
              dependencies=[Depends(get_engine)])
add_pagination(app)
app.include_router(auth_router)
app.include_router(trend_router)
app.include_router(trend_params_router)
app.include_router(trend_data_router)
app.include_router(template_router)
app.include_router(trend_defs_router)
app.include_router(events_router)
app.include_router(event_defs_router)
app.include_router(link_router)
app.include_router(node_router)
app.include_router(unit_router)
app.include_router(trend_groups_router)
app.include_router(trend_writer_router)
app.include_router(simulation_router)
app.include_router(simulation_defs_router)
app.include_router(simulation_data_router)
app.include_router(simulation_params_router)
app.include_router(leak_detector_router)
app.include_router(pipeline_router)
app.include_router(pipeline_params_router)
app.include_router(method_router)
app.include_router(method_def_router)

origins = ['http://localhost:8080',
           'http://192.168.30.52:3000',
           'http://localhost:3000']

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    error = api.Error(code=exc.status_code, message=exc.detail)
    return JSONResponse(content=error.model_dump(), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    err = exc.errors()[0]['ctx']['error']
    error = api.Error(code=status.HTTP_422_UNPROCESSABLE_ENTITY, message=str(err))
    return JSONResponse(content=error.model_dump(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
