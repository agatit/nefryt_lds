from fastapi import FastAPI
from .routers import events_router


app = FastAPI(title='Nefryt LDS API')
app.include_router(events_router)
