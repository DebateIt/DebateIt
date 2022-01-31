from fastapi import Depends, FastAPI

from .routers import Utils
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(Utils.router)
