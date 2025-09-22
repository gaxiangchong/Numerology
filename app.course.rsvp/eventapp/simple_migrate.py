#!/usr/bin/env python3
"""
Simple database migration script to add new columns
"""

import sqlite3
import os

def migrate_database():
    """Add new columns to existing database tables."""
    print("🔄 Starting database migration...")
    
    # Database file path
    db_path = "instance/eventapp.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found. Please run the app first to create the database.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if new columns exist and add them if they don't
        print("📋 Checking and adding new columns...")
        
        # Add membership_grade to User table
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN membership_grade VARCHAR(20) DEFAULT 'Classic'")
            print("✅ Added membership_grade column to User table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️  membership_grade column already exists in User table")
            else:
                print(f"❌ Error adding membership_grade: {e}")
        
        # Add price to Event table
        try:
            cursor.execute("ALTER TABLE event ADD COLUMN price FLOAT DEFAULT 0.0")
            print("✅ Added price column to Event table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️  price column already exists in Event table")
            else:
                print(f"❌ Error adding price: {e}")
        
        # Add payment-related columns to RSVP table
        try:
            cursor.execute("ALTER TABLE rsvp ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending'")
            print("✅ Added payment_status column to RSVP table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️  payment_status column already exists in RSVP table")
            else:
                print(f"❌ Error adding payment_status: {e}")
        
        try:
            cursor.execute("ALTER TABLE rsvp ADD COLUMN payment_amount FLOAT DEFAULT 0.0")
            print("✅ Added payment_amount column to RSVP table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️  payment_amount column already exists in RSVP table")
            else:
                print(f"❌ Error adding payment_amount: {e}")
        
        try:
            cursor.execute("ALTER TABLE rsvp ADD COLUMN stripe_payment_intent_id VARCHAR(200)")
            print("✅ Added stripe_payment_intent_id column to RSVP table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️  stripe_payment_intent_id column already exists in RSVP table")
            else:
                print(f"❌ Error adding stripe_payment_intent_id: {e}")
        
        try:
            cursor.execute("ALTER TABLE rsvp ADD COLUMN receipt_url VARCHAR(500)")
            print("✅ Added receipt_url column to RSVP table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️  receipt_url column already exists in RSVP table")
            else:
                print(f"❌ Error adding receipt_url: {e}")
        
        # Commit changes
        conn.commit()
        print("✅ Database migration completed successfully!")
        
        # Verify the changes
        print("\n🔍 Verifying database schema...")
        cursor.execute("PRAGMA table_info(user)")
        user_columns = [row[1] for row in cursor.fetchall()]
        print(f"User table columns: {user_columns}")
        
        cursor.execute("PRAGMA table_info(event)")
        event_columns = [row[1] for row in cursor.fetchall()]
        print(f"Event table columns: {event_columns}")
        
        cursor.execute("PRAGMA table_info(rsvp)")
        rsvp_columns = [row[1] for row in cursor.fetchall()]
        print(f"RSVP table columns: {rsvp_columns}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
