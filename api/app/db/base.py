# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import BaseTable  # noqa
from app.monitors.db import Monitor, Check
