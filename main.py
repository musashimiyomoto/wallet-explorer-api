from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import wallet
from broker import broker
from exceptions.explorers import ExplorerError
from settings.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """FastAPI lifespan.

    Args:
        app: FastAPI instance.

    """
    setup_logging()

    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()


app = FastAPI(
    title="Wallet Explorer API",
    version="1.0.0",
    description="API for getting information about wallets",
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(exc_class_or_status_code=ExplorerError)
async def explorer_error_handler(request: Request, exc: ExplorerError) -> JSONResponse:
    """Explorer error handler.

    Args:
        request: The request.
        exc: The exception.

    Returns:
        The JSON response.

    """
    return JSONResponse(content={"detail": exc.message}, status_code=exc.status_code)


app.include_router(router=wallet.router)
