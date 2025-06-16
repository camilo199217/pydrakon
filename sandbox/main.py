from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from sandbox.settings import get_settings
from secureauthapi import setup_secureauthapi
from sandbox.app.services.db import engine

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    # start_scheduler()
    yield


app = FastAPI(
    lifespan=lifespan,
)

setup_secureauthapi(app, settings.SECURE_AUTH_API, engine)
