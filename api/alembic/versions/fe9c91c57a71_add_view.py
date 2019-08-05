"""add view

Revision ID: fe9c91c57a71
Revises: 38a093f374d7
Create Date: 2019-08-05 06:15:38.230650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe9c91c57a71'
down_revision = '38a093f374d7'
branch_labels = None
depends_on = None


def upgrade():
    sql = """
	CREATE VIEW check_required AS SELECT
	monitor.id, monitor.name, monitor.endpoint,
	MAX(ck.check_time) as last_checked
	FROM monitor
	LEFT JOIN check_status AS ck ON ck.monitor_id = monitor.id
	GROUP BY monitor.id HAVING coalesce(MAX(ck.check_time) < date_trunc('minute', now()) - interval '4m', true) = true;
    """
    op.execute(sql)


def downgrade():
    down_sql = """
    DROP VIEW check_required;
    """
    op.execute(down_sql)
