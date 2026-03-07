# Numerology Dashboard (separate admin app)

Standalone dashboard that uses the **same database** as the main app. No admin routes or UI in the main app for better security.

## Setup

1. **Same DB as main app**  
   Set the same database URL when running the dashboard:
   - `DATABASE_URL` or `SQLALCHEMY_DATABASE_URI` (e.g. `sqlite:///path/to/mysite/users.db` or your production DB URL).
   - For local SQLite next to mysite: run from repo root and set  
     `SQLALCHEMY_DATABASE_URI=sqlite:///mysite/users.db`  
     (or use the same value as in the main app `.env`).

2. **Secret key**  
   Set `DASHBOARD_SECRET_KEY` (or `SECRET_KEY`) for session security.

3. **Create first admin** (one-time):
   ```bash
   cd dashboard
   # Windows (PowerShell):
   $env:FLASK_APP="app"
   $env:SQLALCHEMY_DATABASE_URI="sqlite:///../mysite/users.db"
   python -c "from app import app; from models import db, bcrypt, DashboardAdmin; ctx = app.app_context(); ctx.push(); db.create_all(); admin = DashboardAdmin(email='your@email.com', password_hash=bcrypt.generate_password_hash('YourSecurePassword').decode()); db.session.add(admin); db.session.commit(); print('Admin created.')"
   ```
   Or from project root with same DB as main app:
   ```bash
   set FLASK_APP=dashboard.app
   set SQLALCHEMY_DATABASE_URI=sqlite:///mysite/users.db
   flask run --port 8051
   ```
   Then create admin via Python as above (with app import path `dashboard.app` and same DB).

## Run

```bash
cd NumberEnergy
set FLASK_APP=dashboard.app
set DATABASE_URL=sqlite:///mysite/users.db
set DASHBOARD_SECRET_KEY=your-secret-key
flask run --port 8051
```

Or:

```bash
cd NumberEnergy/dashboard
set FLASK_APP=app
set SQLALCHEMY_DATABASE_URI=sqlite:///../mysite/users.db
flask run --port 8051
```

Open http://127.0.0.1:8051 and log in with your dashboard admin email and password.

## Features

- **Home**: Total users, paid subscribers, referrals, vouchers available.
- **Subscribers**: List users, search by email/phone, filter by plan.
- **Vouchers**: List and create vouchers (code, discount %, valid from/until).
- **Top up credits**: Add usage credits to any user by email.
- **Orders**: List pending/paid orders.

Dashboard auth is separate from the main app (table `dashboard_admin`). Main app no longer exposes any admin UI or routes.
