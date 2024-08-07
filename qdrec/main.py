from dataclasses import dataclass

from fastapi import FastAPI

from qdrec.api.querido_diario.routers import excerpts

from qdrec.database.connection import SessionLocal, engine

app = FastAPI()

app.include_router(excerpts.router)