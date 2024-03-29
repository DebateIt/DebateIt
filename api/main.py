from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import Nlp, Utils, Topics, Users, Auth, Debates, RoomMessage
from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Utils.router)
app.include_router(Topics.router)
app.include_router(Users.router)
app.include_router(Auth.router)
app.include_router(Debates.router)
app.include_router(Nlp.router)
app.include_router(RoomMessage.router)
