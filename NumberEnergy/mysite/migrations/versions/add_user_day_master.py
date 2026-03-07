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


def upgrade():
    op.add_column('user', sa.Column('day_master', sa.String(length=10), nullable=True))


def downgrade():
    op.drop_column('user', 'day_master')
