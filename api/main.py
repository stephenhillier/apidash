"""
Main application entrypoint that initializes FastAPI
"""
from typing import List

import databases
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import DATABASE_URI
from app import monitors_db as mon_repo
from app import monitors as monitors_v1

database = databases.Database(DATABASE_URI)

app = FastAPI(title="API Dash", openapi_url="/api/v1/openapi.json")

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """ run on app startup - get database connection """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """ run on shutdown """
    await database.disconnect()

@app.get("/api/v1/monitors", response_model=List[monitors_v1.Monitor])
async def list_monitors():
    """ list active monitors """
    monitors = await mon_repo.list_monitors(database)
    return monitors

@app.post("/api/v1/monitors", response_model=monitors_v1.Monitor)
async def new_monitor(monitor: monitors_v1.MonitorRequest):
    """ create a new monitors """
    monitors = await mon_repo.create_monitor(database, monitor)
    return monitors
