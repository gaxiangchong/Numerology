# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from extensions import db
from sqlalchemy import UniqueConstraint  # ✅ add this line

import uuid

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_pro = db.Column(db.Boolean, default=False)
    pro_until = db.Column(db.DateTime, nullable=True)
    referral_code = db.Column(db.String(20), nullable=True)  # <-- remove unique=True here
    referred_by = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pro_until = db.Column(db.DateTime, nullable=True)
    stripe_subscription_id = db.Column(db.String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint('referral_code', name='uq_user_referral_code'),  # ✅ named constraint
    )