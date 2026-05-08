import asyncio
from .app import init_app
import uvicorn

if __name__ == '__main__':
    app = asyncio.run(init_app())
    uvicorn.run(app, host="0.0.0.0", port=8000)
