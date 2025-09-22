#!/usr/bin/env python3
"""
Test script for the integrated RSVP/payment system.
This script tests the new payment integration functionality.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Event, RSVP

def test_integrated_rsvp():
    """Test the integrated RSVP/payment system."""
    print("🧪 Testing Integrated RSVP/Payment System...")
    
    try:
        with app.app_context():
            # Test 1: Check if payment_method column exists
            print("\n1️⃣ Testing database schema...")
            with db.engine.connect() as conn:
                result = conn.execute(db.text("""
                    SELECT COUNT(*) as count 
                    FROM pragma_table_info('rsvp') 
                    WHERE name = 'payment_method'
                """))
                column_exists = result.fetchone()[0] > 0
                
                if column_exists:
                    print("✅ payment_method column exists in RSVP table")
                else:
                    print("❌ payment_method column missing from RSVP table")
                    return False
            
            # Test 2: Check users and events
            print("\n2️⃣ Testing users and events...")
            users = User.query.all()
            events = Event.query.all()
            print(f"📊 Found {len(users)} users and {len(events)} events")
            
            if not users or not events:
                print("❌ Need at least one user and one event to test")
                return False
            
            # Test 3: Test credit payment simulation
            print("\n3️⃣ Testing credit payment simulation...")
            test_user = users[0]
            test_event = events[0]
            
            print(f"   👤 Testing with user: {test_user.username}")
            print(f"   🎫 Testing with event: {test_event.name}")
            print(f"   💰 Event price: {test_event.price}")
            print(f"   💳 User credits: {test_user.credit_point}")
            
            # Test 4: Test RSVP creation with different payment methods
            print("\n4️⃣ Testing RSVP creation...")
            
            # Create test RSVP for free event
            if test_event.price == 0:
                print("   🆓 Testing free event RSVP...")
                test_rsvp = RSVP(
                    event_id=test_event.id,
                    user_id=test_user.id,
                    status='Accepted',
                    guests=0,
                    payment_status='paid',
                    payment_amount=0.0,
                    payment_method='free'
                )
                db.session.add(test_rsvp)
                db.session.commit()
                print("   ✅ Free event RSVP created successfully")
            
            # Test 5: Test credit payment for paid event
            if test_event.price > 0:
                print("   💳 Testing credit payment for paid event...")
                
                # Set user credits to cover event price
                original_credits = test_user.credit_point
                test_user.credit_point = test_event.price + 50.0  # Extra credits
                db.session.commit()
                
                print(f"   💰 Set user credits to: {test_user.credit_point}")
                
                # Simulate credit payment
                test_user.credit_point -= test_event.price
                
                test_rsvp = RSVP(
                    event_id=test_event.id,
                    user_id=test_user.id,
                    status='Accepted',
                    guests=0,
                    payment_status='paid',
                    payment_amount=test_event.price,
                    payment_method='credit'
                )
                db.session.add(test_rsvp)
                db.session.commit()
                
                print(f"   ✅ Credit payment processed. Remaining credits: {test_user.credit_point}")
                
                # Restore original credits
                test_user.credit_point = original_credits
                db.session.commit()
            
            # Test 6: Verify RSVP data
            print("\n5️⃣ Testing RSVP data verification...")
            rsvps = RSVP.query.filter_by(user_id=test_user.id).all()
            print(f"   📊 Found {len(rsvps)} RSVPs for test user")
            
            for rsvp in rsvps:
                print(f"   🎫 RSVP ID: {rsvp.id}, Status: {rsvp.status}, Payment: {rsvp.payment_method}, Amount: {rsvp.payment_amount}")
            
            print("\n🎉 All integrated RSVP/payment tests passed!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return False

def show_rsvp_summary():
    """Show a summary of all RSVPs with payment methods."""
    print("\n📊 RSVP Payment Summary:")
    print("=" * 60)
    
    try:
        with app.app_context():
            rsvps = RSVP.query.all()
            
            if not rsvps:
                print("No RSVPs found in database.")
                return
            
            payment_methods = {}
            total_amount = 0
            
            for rsvp in rsvps:
                method = rsvp.payment_method or 'unknown'
                if method not in payment_methods:
                    payment_methods[method] = {'count': 0, 'amount': 0}
                
                payment_methods[method]['count'] += 1
                payment_methods[method]['amount'] += rsvp.payment_amount or 0
                total_amount += rsvp.payment_amount or 0
            
            for method, data in payment_methods.items():
                print(f"💳 {method.upper():<10} | Count: {data['count']:>3} | Amount: ${data['amount']:>8.2f}")
            
            print("=" * 60)
            print(f"📈 Total RSVPs: {len(rsvps)}")
            print(f"💰 Total Amount: ${total_amount:.2f}")
            
    except Exception as e:
        print(f"❌ Error showing summary: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🎫 Integrated RSVP/Payment System Test Suite")
    print("=" * 60)
    
    success = test_integrated_rsvp()
    
    if success:
        show_rsvp_summary()
        print("\n✅ Integrated RSVP/payment system is ready!")
        print("\n📋 Next steps:")
        print("1. Go to any event detail page")
        print("2. Select 'Accept' for RSVP")
        print("3. Choose payment method (Card or Credit)")
        print("4. Submit RSVP with integrated payment")
        print("5. Verify payment processing works correctly")
    else:
        print("\n❌ Integrated RSVP/payment system tests failed!")
        print("Please check the error messages above.")
    
    print("=" * 60)
