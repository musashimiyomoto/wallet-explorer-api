from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import wallet

app = FastAPI(
    title="TRON Wallet API",
    version="1.0.0",
    description="API for getting information about TRON wallets",
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=wallet.router)
