from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from .db import get_engine
from .routers import (events_router, event_defs_router, trend_defs_router, trend_router, auth_router, link_router,
                      node_router)


app = FastAPI(title='Nefryt LDS API',
              dependencies=[Depends(get_engine)])
app.include_router(events_router)
app.include_router(event_defs_router)
app.include_router(trend_defs_router)
app.include_router(trend_router)
app.include_router(auth_router)
app.include_router(link_router)
app.include_router(node_router)


origins = ['http://localhost:8080',
           'http://192.168.30.52:3000']

app.add_middleware(
    CORSMiddleware, # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
