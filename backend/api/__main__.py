from fastapi import FastAPI
from .routers import events_router, event_defs_router, trend_defs_router


app = FastAPI(title='Nefryt LDS API')
app.include_router(events_router)
app.include_router(event_defs_router)
app.include_router(trend_defs_router)

