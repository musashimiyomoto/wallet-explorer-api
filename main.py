from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import wallet
from broker import broker
from exceptions.explorers import ExplorerError

app = FastAPI(
    title="Wallet Explorer API",
    version="1.0.0",
    description="API for getting information about wallets",
    redoc_url=None,
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ExplorerError)
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


async def startup_event() -> None:
    """Startup event."""
    await broker.startup()


async def shutdown_event() -> None:
    """Shutdown event."""
    await broker.shutdown()


app.add_event_handler(event_type="startup", func=startup_event)
app.add_event_handler(event_type="shutdown", func=shutdown_event)
