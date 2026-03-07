# Dashboard models: DashboardAdmin (own auth) + mirrors of main app tables for read/write.
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class DashboardAdmin(db.Model):
    """Dashboard-only admin users. Separate from main app User table."""
    __tablename__ = 'dashboard_admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Mirror of main app User table (same column names we need for dashboard).
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_pro = db.Column(db.Boolean, default=False)
    pro_until = db.Column(db.DateTime, nullable=True)
    plan = db.Column(db.String(20), default='free')
    credits_balance = db.Column(db.Integer, default=0)
    credits_per_month = db.Column(db.Integer, default=10)
    credit_reset_at = db.Column(db.DateTime, nullable=True)
    referral_code = db.Column(db.String(20), nullable=True)
    referred_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    stripe_subscription_id = db.Column(db.String(100), nullable=True)
    display_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    day_master = db.Column(db.String(10), nullable=True)
    mail_subscriber = db.Column(db.Boolean, default=False, nullable=False)


class Voucher(db.Model):
    __tablename__ = 'voucher'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(20), default='AVAILABLE')
    discount_percent = db.Column(db.Integer, nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, nullable=True)
    used_at = db.Column(db.DateTime, nullable=True)
    used_by_id = db.Column(db.Integer, nullable=True)


class UsageCreditEntry(db.Model):
    __tablename__ = 'usage_credit_entry'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reference_type = db.Column(db.String(50), nullable=True)
    reference_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PendingOrder(db.Model):
    __tablename__ = 'pending_order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    plan = db.Column(db.String(20), nullable=False)
    amount_cents = db.Column(db.Integer, nullable=False)
    credit_applied_cents = db.Column(db.Integer, default=0)
    voucher_id = db.Column(db.Integer, nullable=True)
    stripe_session_id = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)


class ReferralCreditGrant(db.Model):
    __tablename__ = 'referral_credit_grant'
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, nullable=False)
    referred_user_id = db.Column(db.Integer, nullable=False)
    amount_cents = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
