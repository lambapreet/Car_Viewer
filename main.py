from fastapi import FastAPI
from .routers import car_view


app = FastAPI()


app.include_router(car_view.router)