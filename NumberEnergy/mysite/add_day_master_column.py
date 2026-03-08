"""
One-off: Add day_master column to user table.
Uses the same DB config as the web app (from .env / env vars).

Run from mysite:  python add_day_master_column.py

If Web app uses DATABASE_URL from PythonAnywhere Web tab (not .env),
export it first:  export DATABASE_URL="sqlite:////home/bazipro/numerology-app/mysite/instance/users.db"
"""
import os
import sys

mysite = os.path.dirname(os.path.abspath(__file__))
if mysite not in sys.path:
    sys.path.insert(0, mysite)
os.chdir(mysite)

# Load env before app (app loads .env too)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(mysite, '.env'))
    load_dotenv(os.path.join(os.path.dirname(mysite), '.env'))
except ImportError:
    pass

from app import app
from extensions import db
from sqlalchemy import text

def main():
    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"DB: {db_uri}")
        conn = db.engine.connect()
        try:
            r = conn.execute(text("PRAGMA table_info(user)"))
            cols = [row[1] for row in r.fetchall()]
            if 'day_master' in cols:
                print("day_master already exists. Done.")
                return
            conn.execute(text("ALTER TABLE user ADD COLUMN day_master VARCHAR(10)"))
            conn.commit()
            print("Added user.day_master successfully.")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
