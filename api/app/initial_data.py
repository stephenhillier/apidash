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
    mon = MonitorFactory()
    logger.info(f"Adding monitor {mon.name}")
    db_session.add(mon)
    db_session.commit()


def main():
    logger.info("Creating initial fixture data")
    create_monitor()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
