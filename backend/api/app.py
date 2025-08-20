from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from config import setup_engine
from db import get_engine
from .routers import (events_router, event_defs_router, trend_defs_router, trend_router, auth_router, link_router,
                      node_router, template_router, unit_router, trend_groups_router, trend_writer_router,
                      simulation_router, trend_params_router, trend_data_router)
from .schemas import Error

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
    error = Error(code=exc.status_code, message=exc.detail)
    return JSONResponse(content=error.model_dump(), status_code=exc.status_code)
