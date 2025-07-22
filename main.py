from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routers import (
    admin,
    auth,
    category,
    client,
    delivery,
    dish,
    order,
    schedule,
    user,
)

app = FastAPI(title="Restoranchiki API")

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")

# Client
app.include_router(router=auth.router)
app.include_router(router=category.router)
app.include_router(router=client.router)
app.include_router(router=dish.router)
app.include_router(router=order.router)
app.include_router(router=schedule.router)
app.include_router(router=user.router)
app.include_router(router=delivery.router)

# Admin
app.include_router(router=admin.router)
