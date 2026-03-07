"""One-time script to create the first dashboard admin. Run from dashboard dir with same DB as main app."""
import os
import sys

# Ensure we can load app and config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, bcrypt, DashboardAdmin

def main():
    email = os.environ.get('DASHBOARD_ADMIN_EMAIL') or input('Admin email: ').strip()
    password = os.environ.get('DASHBOARD_ADMIN_PASSWORD') or input('Admin password: ').strip()
    if not email or not password:
        print('Email and password required.')
        return 1
    with app.app_context():
        db.create_all()
        if DashboardAdmin.query.filter_by(email=email).first():
            print('Admin with this email already exists.')
            return 0
        admin = DashboardAdmin(
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
        )
        db.session.add(admin)
        db.session.commit()
        print(f'Dashboard admin created: {email}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
