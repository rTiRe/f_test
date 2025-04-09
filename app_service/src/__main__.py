from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from config import logger
from src.api import router


logger = logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(router)
    return app


if __name__ == '__main__':
    uvicorn.run(
        'src.__main__:create_app',
        factory=True,
        host='0.0.0.0',
        port=8001,
        workers=1,
    )
