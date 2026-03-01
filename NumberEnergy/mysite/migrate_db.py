"""
One-time migration: add referred_by_id, is_admin to user table and create new tables.
Run from NumberEnergy/mysite:  python migrate_db.py
Or from NumberEnergy:         python mysite/migrate_db.py
"""
import os
import sys

# Ensure mysite is on path when run from NumberEnergy
if __name__ == "__main__":
    mysite = os.path.dirname(os.path.abspath(__file__))
    if mysite not in sys.path:
        sys.path.insert(0, mysite)
    os.chdir(mysite)

from app import app
from extensions import db
from sqlalchemy import text

def column_exists(conn, table, column):
    """SQLite: check if column exists in table."""
    r = conn.execute(text(f"PRAGMA table_info({table})"))
    return any(row[1] == column for row in r.fetchall())

def table_exists(conn, name):
    r = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name=:n"), {"n": name})
    return r.fetchone() is not None

def run_migration():
    with app.app_context():
        conn = db.engine.connect()
        try:
            # 1) Add missing columns to user
            if not column_exists(conn, "user", "referred_by_id"):
                conn.execute(text("ALTER TABLE user ADD COLUMN referred_by_id INTEGER REFERENCES user(id)"))
                conn.commit()
                print("Added user.referred_by_id")
            else:
                print("user.referred_by_id already exists")

            if not column_exists(conn, "user", "is_admin"):
                conn.execute(text("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
                conn.commit()
                print("Added user.is_admin")
            else:
                print("user.is_admin already exists")

            # 2) Create new tables if they don't exist (create_all only creates missing tables)
            db.create_all()
            print("Ensured all tables exist (credit_ledger_entry, voucher, referral_credit_grant, pending_order, password_reset_token).")

            # 3) Optional: set first user as admin (uncomment and set email if you want)
            # from models import User
            # u = User.query.filter_by(email='your@email.com').first()
            # if u:
            #     u.is_admin = True
            #     db.session.commit()
            #     print('Set admin for', u.email)
        finally:
            conn.close()
    print("Migration done.")

if __name__ == "__main__":
    run_migration()
