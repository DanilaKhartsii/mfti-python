from fastapi import FastAPI

from .database import Base, engine
from . import models
from .auth import router as auth_router
from .students import router as students_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students API with Auth")

app.include_router(auth_router)
app.include_router(students_router)
