""" database tables and operations for monitors """

import sqlalchemy
from databases import Database
from app.db.base_class import BaseTable
from app import monitors as monitors_v1

metadata = sqlalchemy.MetaData()

class Monitor(BaseTable):
    """ a monitor represents a re-occuring check against an endpoint """
    __tablename__ = "monitor"

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    endpoint = sqlalchemy.Column(sqlalchemy.String)

monitor = Monitor.__table__

async def create_monitor(db: Database, mon: monitors_v1.Monitor):
    """ creates a new monitor in the database """

    query = monitor.insert().values(name=mon.name, endpoint=mon.endpoint)
    return await db.execute(query)

async def list_monitors(db: Database):
    """ lists all monitors """

    query = monitor.select()
    return await db.fetch_all(query)
