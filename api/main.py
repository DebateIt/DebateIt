from fastapi import Depends, FastAPI

from .routers import Utils, Topics, Users, Auth, Debates
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(Utils.router)
app.include_router(Topics.router)
app.include_router(Users.router)
app.include_router(Auth.router)
app.include_router(Debates.router)
