""" database tables and operations for monitors """
import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, MetaData, Integer, Boolean
from sqlalchemy.orm import relationship
from databases import Database
from app.db.base_class import BaseTable
from app.monitors import models as monitors_v1

metadata = MetaData()

class Monitor(BaseTable):
    """ a monitor represents a re-occuring check against an endpoint """
    __tablename__ = "monitor"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    create_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    expire_time = Column(DateTime, nullable=True)
    checks = relationship("Check", back_populates="monitor")

class Check(BaseTable):
    """ a check is a single check request made for a monitor """
    __tablename__ = "check_status"

    id = Column(BigInteger, primary_key=True)
    monitor_id = Column(BigInteger, ForeignKey('monitor.id'), nullable=False)
    check_time = Column(DateTime, nullable=False)
    status_code = Column(Integer, nullable=False)
    schema_valid = Column(Boolean)  # can be null if no schema defined
    monitor = relationship("Monitor", back_populates="checks")

monitor = Monitor.__table__
check = Check.__table__


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

async def get_last_seven_days(db: Database, monitor_id: int):
    query = """
    SELECT 
    """