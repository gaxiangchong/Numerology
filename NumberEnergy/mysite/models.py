# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from extensions import db
from sqlalchemy import UniqueConstraint

import uuid
import secrets

#db = SQLAlchemy()

def _generate_referral_code():
    return secrets.token_urlsafe(6).upper().replace("-", "")[:8]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_pro = db.Column(db.Boolean, default=False)  # kept for backward compat; paid = (plan in ('monthly','annual'))
    pro_until = db.Column(db.DateTime, nullable=True)
    # Credit-based plans: free=10/mo, monthly=50/mo (RM19.90), annual=100/mo (RM199)
    plan = db.Column(db.String(20), default='free')  # 'free' | 'monthly' | 'annual'
    credits_balance = db.Column(db.Integer, default=0)
    credits_per_month = db.Column(db.Integer, default=10)
    credit_reset_at = db.Column(db.DateTime, nullable=True)
    referral_code = db.Column(db.String(20), nullable=True)
    referred_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # referrer user id
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stripe_subscription_id = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    display_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(30), nullable=True)

    __table_args__ = (
        UniqueConstraint('referral_code', name='uq_user_referral_code'),
    )

    referrer = db.relationship('User', remote_side=[id], foreign_keys=[referred_by_id], backref=db.backref('referred_users', lazy='dynamic'))

class UserHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    input_data = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('history', lazy=True))


class CreditLedgerEntry(db.Model):
    """Append-only store credit ledger. Balance = sum(CREDIT) - sum(DEBIT) + sum(REVERSAL)."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # CREDIT | DEBIT | REVERSAL
    amount_cents = db.Column(db.Integer, nullable=False)  # always positive
    reference_type = db.Column(db.String(50), nullable=True)  # referral | admin_grant | purchase | reversal
    reference_id = db.Column(db.String(100), nullable=True)
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('credit_entries', lazy='dynamic'))


class Voucher(db.Model):
    """Voucher codes. Never delete; use status EXPIRED/REVOKED."""
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(20), default='AVAILABLE')  # AVAILABLE | USED | EXPIRED | REVOKED
    discount_percent = db.Column(db.Integer, nullable=False)  # 1-100
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    used_at = db.Column(db.DateTime, nullable=True)
    used_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class ReferralCreditGrant(db.Model):
    """Idempotency: one store-credit grant per (referrer, referred_user)."""
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount_cents = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    referrer = db.relationship('User', foreign_keys=[referrer_id])
    referred_user = db.relationship('User', foreign_keys=[referred_user_id])
    __table_args__ = (UniqueConstraint('referrer_id', 'referred_user_id', name='uq_referral_grant'),)


class UsageCreditEntry(db.Model):
    """Append-only usage credits: balance = sum(amount). Types: monthly_grant, number_analysis, ai_request, referral_bonus."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # positive = credit, negative = debit
    reference_type = db.Column(db.String(50), nullable=True)
    reference_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('usage_credit_entries', lazy='dynamic'))


class ReferralUsageCreditGrant(db.Model):
    """Idempotency: one usage-credit grant per (referrer, referred_user) when referred user subscribes."""
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan = db.Column(db.String(20), nullable=False)  # monthly | annual
    credits_granted = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('referrer_id', 'referred_user_id', name='uq_referral_usage_grant'),)


class PasswordResetToken(db.Model):
    """One-time token for forgot-password flow. Expires after RESET_EXPIRY."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref=db.backref('password_reset_tokens', lazy='dynamic'))


class PendingOrder(db.Model):
    """Tracks checkout: credit/voucher applied, Stripe session; fulfilled on payment success."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan = db.Column(db.String(20), nullable=False)  # monthly | annual
    amount_cents = db.Column(db.Integer, nullable=False)  # amount charged (Stripe or 0)
    credit_applied_cents = db.Column(db.Integer, default=0)
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'), nullable=True)
    stripe_session_id = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending | paid | failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref=db.backref('pending_orders', lazy='dynamic'))
    voucher = db.relationship('Voucher', backref=db.backref('orders_using', lazy=True))