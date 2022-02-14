from fastapi import Depends, FastAPI

from .routers import Utils, Users, Auth
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(Utils.router)
app.include_router(Users.router)
app.include_router(Auth.router)
