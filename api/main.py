"""
Main application entrypoint that initializes FastAPI
"""
from typing import List

import databases
from fastapi import FastAPI, HTTPException
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware

from app.config import DATABASE_URI
from app.monitors import db as mon_repo
from app.monitors import models as monitors_v1

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

@app.delete("/api/v1/monitors/{monitor_id}")
async def delete_monitor(monitor_id: int):
    """ delete a monitor """

    # check if monitor exists, and return 404 if it doesn't
    mon = await mon_repo.get_monitor(database, monitor_id)
    if not mon:
        return HTTPException(status_code=404, detail="Monitor not found")

    # monitor exists, delete it
    await mon_repo.delete_monitor(database, monitor_id)

    return Response(status_code=204, content=b"")
