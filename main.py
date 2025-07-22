from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import wallet
from exceptions.explorers import ExplorerError

app = FastAPI(
    title="Wallet Explorer API",
    version="1.0.0",
    description="API for getting information about wallets",
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
    return JSONResponse(content=exc.message, status_code=exc.status_code)


app.include_router(router=wallet.router)
