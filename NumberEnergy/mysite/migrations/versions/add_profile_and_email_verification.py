"""Add profile fields, email verification, referral profile-complete grant

Revision ID: add_profile_verify
Revises: add_lucky_fav
Create Date: 2026-02-28

"""
from alembic import op
import sqlalchemy as sa


revision = 'add_profile_verify'
down_revision = 'add_lucky_fav'
branch_labels = None
depends_on = None


def _table_exists(conn, name):
    r = conn.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table' AND name=:n"), {"n": name})
    return r.scalar() is not None


def upgrade():
    conn = op.get_bind()
    # Add user columns (skip if already present)
    try:
        op.add_column('user', sa.Column('email_verified', sa.Boolean(), nullable=False, server_default=sa.false()))
        op.execute('UPDATE user SET email_verified = 1')
    except Exception:
        pass
    for col, col_sa in [
        ('profile_completed', sa.Column('profile_completed', sa.Boolean(), nullable=False, server_default=sa.false())),
        ('occupation', sa.Column('occupation', sa.String(length=100), nullable=True)),
        ('date_of_birth', sa.Column('date_of_birth', sa.Date(), nullable=True)),
        ('nationality', sa.Column('nationality', sa.String(length=80), nullable=True)),
        ('income_range', sa.Column('income_range', sa.String(length=50), nullable=True)),
        ('income_currency', sa.Column('income_currency', sa.String(length=10), nullable=True)),
        ('phone_country_code', sa.Column('phone_country_code', sa.String(length=10), nullable=True)),
    ]:
        try:
            op.add_column('user', col_sa)
        except Exception:
            pass

    if not _table_exists(conn, 'email_verification_token'):
        op.create_table(
            'email_verification_token',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('token', sa.String(length=64), nullable=False),
            sa.Column('expires_at', sa.DateTime(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('used_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('token', name='uq_email_verification_token_token')
        )

    if not _table_exists(conn, 'referral_profile_complete_grant'):
        op.create_table(
            'referral_profile_complete_grant',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('referrer_id', sa.Integer(), nullable=False),
            sa.Column('referred_user_id', sa.Integer(), nullable=False),
            sa.Column('credits_granted', sa.Integer(), nullable=False, server_default='25'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['referrer_id'], ['user.id'], ),
            sa.ForeignKeyConstraint(['referred_user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('referrer_id', 'referred_user_id', name='uq_referral_profile_complete')
        )


def downgrade():
    op.drop_table('referral_profile_complete_grant')
    op.drop_table('email_verification_token')
    op.drop_column('user', 'phone_country_code')
    op.drop_column('user', 'income_currency')
    op.drop_column('user', 'income_range')
    op.drop_column('user', 'nationality')
    op.drop_column('user', 'date_of_birth')
    op.drop_column('user', 'occupation')
    op.drop_column('user', 'profile_completed')
    op.drop_column('user', 'email_verified')
