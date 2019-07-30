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

async def create_monitor(db: Database, mon: monitors_v1.Monitor) -> monitors_v1.Monitor:
    """ creates a new monitor in the database """

    query = monitor.insert() \
        .values(name=mon.name, endpoint=mon.endpoint) \
        .returning(monitor.c.id, monitor.c.name, monitor.c.endpoint)
    mon = await db.fetch_one(query)
    return monitors_v1.Monitor(**mon)


async def list_monitors(db: Database):
    """ lists all monitors """

    query = monitor.select()
    mon_list = await db.fetch_all(query)
    return [monitors_v1.Monitor(**mon) for mon in mon_list]

async def delete_monitor(db: Database, monitor_id: int):
    """ deletes a monitor """

    query = monitor.delete().where(monitor.c.id == monitor_id)
    return await db.execute(query)

async def get_monitor(db: Database, monitor_id: int):
    """ get a single monitor """

    query = monitor.select().where(monitor.c.id == monitor_id)
    return await db.fetch_one(query)