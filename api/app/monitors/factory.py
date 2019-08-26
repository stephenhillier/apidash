"""
creates test data for monitors and checks
"""
import factory
import datetime
from app.db.session import db_session

from app.monitors import db as monitors_db


STATUS_CODE_LIST = [200] * 99 + [500]


class CheckFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ factory to generate checks """

    _status_int = factory.Faker('pyint', min_value=0, max_value=99, step=1)

    monitor_id = None
    check_time = factory.Sequence(
        lambda n: datetime.datetime.now() - datetime.timedelta(hours=1*n))
    status_code = factory.LazyAttribute(
        lambda o: STATUS_CODE_LIST[o._status_int])
    latency = factory.Faker('pyint', min_value=4, max_value=20, step=1)

    class Meta:
        model = monitors_db.Check
        sqlalchemy_session = db_session
        exclude = "_status_int"


class MonitorFactory(factory.alchemy.SQLAlchemyModelFactory):
    """ factory to generate a monitor """
    name = "Users list"
    endpoint = "http://apidash.dev:8000/api/v1/status/200"
    checks = factory.RelatedFactoryList(CheckFactory, 'monitor', size=24*7)

    class Meta:
        model = monitors_db.Monitor
        sqlalchemy_session = db_session
