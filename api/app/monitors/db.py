""" database tables and operations for monitors """
import datetime
import logging
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, MetaData, Integer, Boolean
from sqlalchemy.orm import relationship
from databases import Database
from app.db.base_class import BaseTable
from app.monitors import models as monitors_v1

logger = logging.getLogger("api")

metadata = MetaData()


class Monitor(BaseTable):
    """ a monitor represents a re-occuring check against an endpoint """
    __tablename__ = "monitor"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    create_time = Column(DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    expire_time = Column(DateTime, nullable=True)
    checks = relationship("Check", back_populates="monitor",
                          cascade="save-update, merge, delete, delete-orphan")


class Check(BaseTable):
    """ a check is a single check request made for a monitor """
    __tablename__ = "check_status"

    id = Column(BigInteger, primary_key=True)
    monitor_id = Column(BigInteger, ForeignKey('monitor.id'), nullable=False)
    check_time = Column(DateTime, nullable=False, index=True)
    status_code = Column(Integer, nullable=False, default=0)
    schema_valid = Column(Boolean)  # can be null if no schema defined
    monitor = relationship("Monitor", back_populates="checks")


monitor = Monitor.__table__
check = Check.__table__


async def get_summaries(db: Database, monitor_id: int):
    """ get summaries for a group of monitors """

    summary = """
        SELECT day, coalesce(num_fail, 0) AS num_fail, coalesce(num_ok, 0) as num_ok
        FROM (SELECT now()::date -6+d AS day FROM generate_series (0, 6) d) d
        LEFT JOIN (
        SELECT check_time::date AS day,
            count(*) filter (where status_code > 299 or status_code < 100) as num_fail,
            count(*) filter (where status_code >= 200 and status_code <= 299 ) as num_ok
        FROM check_status
        WHERE check_time >= date_trunc('day', now()) - interval '6d'
        AND monitor_id = :monitor_id
        GROUP BY 1
        ) e USING (day);
    """

    values = {"monitor_id": monitor_id}
    summary_rows = await db.fetch_all(summary, values=values)

    weekly = [monitors_v1.DailySummary(
        **dict(x), date=dict(x).get("day")) for x in summary_rows]

    return weekly


async def create_monitor(db: Database, mon: monitors_v1.Monitor) -> monitors_v1.Monitor:
    """ creates a new monitor in the database """

    query = monitor.insert() \
        .values(name=mon.name, endpoint=mon.endpoint, create_time=datetime.datetime.utcnow()) \
        .returning(monitor.c.id, monitor.c.name, monitor.c.endpoint, monitor.c.create_time)
    mon = await db.fetch_one(query)
    return monitors_v1.Monitor(**mon)


async def list_monitors(db: Database):
    """ lists all monitors, with status indicators """

    query = """
        SELECT
        monitor.id, monitor.name, monitor.endpoint,
        MAX(ck.check_time) as last_checked,
        MAX(ck.check_time) filter (where ck.status_code > 299) as last_failed,
        MAX(ck.check_time) filter (where ck.status_code >= 200 and ck.status_code < 300) as last_success,
        CASE
            WHEN MAX(ck.check_time) filter (where ck.status_code > 299) = MAX(ck.check_time) THEN 2
            WHEN MAX(ck.check_time) filter (where ck.status_code > 299) > date_trunc('day', now()) - interval '10m' THEN 1
            ELSE 0
        END AS current_status,
        CASE
            WHEN MAX(ck.check_time) = NULL THEN -1
            WHEN MAX(ck.check_time) filter (where ck.status_code >= 200 and ck.status_code < 300) = MAX(ck.check_time) THEN 0
            ELSE 2
        END AS last_check
        FROM monitor
        LEFT JOIN check_status AS ck ON ck.monitor_id = monitor.id
        GROUP BY monitor.id
    """
    mon_list = await db.fetch_all(query)

    return [monitors_v1.Monitor(**mon, weekly=await get_summaries(db, mon.get('id'))) for mon in mon_list]


async def delete_monitor(db: Database, monitor_id: int):
    """ deletes a monitor """

    query = monitor.delete().where(monitor.c.id == monitor_id)
    return await db.execute(query)


async def get_monitor(db: Database, monitor_id: int):
    """ get single monitor """
    query = monitor.select().where(monitor.c.id == monitor_id)
    return await db.fetch_one(query)


async def get_monitor_status_timeseries(
    db: Database,
    monitor_id: int,
    start_time: datetime.datetime = datetime.datetime.utcnow() - datetime.timedelta(days=7),
    end_time: datetime.datetime = datetime.datetime.utcnow()
):
    """ get the time series data for a single monitor """
    query = check.select() \
        .where(
            check.c.monitor_id == monitor_id,
            check.c.check_time > start_time,
            check.c.check_time < end_time)
    return await db.fetch_all(query)
