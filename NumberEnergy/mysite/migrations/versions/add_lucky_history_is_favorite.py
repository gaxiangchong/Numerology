"""Add is_favorite to lucky_number_history

Revision ID: add_lucky_fav
Revises: add_lucky_hist
Create Date: 2026-02-28

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_lucky_fav'
down_revision = 'add_lucky_hist'
branch_labels = None
depends_on = None


def _column_exists(conn, table, column):
    r = conn.execute(sa.text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in r.fetchall())


def upgrade():
    conn = op.get_bind()
    if not _column_exists(conn, 'lucky_number_history', 'is_favorite'):
        op.add_column('lucky_number_history', sa.Column('is_favorite', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('lucky_number_history', 'is_favorite')
