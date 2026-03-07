"""Add LuckyNumberHistory table for last 10 lucky numbers per user

Revision ID: add_lucky_hist
Revises: add_day_master
Create Date: 2026-03-01

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_lucky_hist'
down_revision = 'add_day_master'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'lucky_number_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('number', sa.String(length=10), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('lucky_number_history')
