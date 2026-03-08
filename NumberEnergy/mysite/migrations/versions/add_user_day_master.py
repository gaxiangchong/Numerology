"""Add user day_master (日柱) for personalized lucky number

Revision ID: add_day_master
Revises: 3de7cc51059f
Create Date: 2026-03-01

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_day_master'
down_revision = '3de7cc51059f'
branch_labels = None
depends_on = None


def _column_exists(conn, table, column):
    """SQLite: check if column exists in table."""
    r = conn.execute(sa.text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in r.fetchall())


def upgrade():
    conn = op.get_bind()
    if not _column_exists(conn, 'user', 'day_master'):
        op.add_column('user', sa.Column('day_master', sa.String(length=10), nullable=True))


def downgrade():
    op.drop_column('user', 'day_master')
