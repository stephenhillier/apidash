import logging
import os
from app.db.session import db_session
from app.monitors.factory import MonitorFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_monitor():
    """generate monitor data"""

    # logger
    logger = logging.getLogger("monitors")
    codes = [200, 200, 200, 500, 404]
    for i in range(5):
        mon = MonitorFactory(
            endpoint=f"http://apidash.dev:8000/api/v1/status/{codes[i]}"
        )
        logger.info(f"Adding monitor {mon.name}")
        db_session.add(mon)
    db_session.commit()


def main():
    logger.info("Creating initial fixture data")
    create_monitor()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
