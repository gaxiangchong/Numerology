#!/usr/bin/env python3
"""
Create dummy feedback data for testing the feedback analytics system
This script generates realistic feedback data for existing events
"""

import os
import sys
import random
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Event, User, RSVP, Feedback

def create_dummy_feedback():
    """Create dummy feedback data for testing"""
    print("🎭 Creating Dummy Feedback Data")
    print("=" * 40)
    
    with app.app_context():
        # Get all events
        events = Event.query.all()
        if not events:
            print("❌ No events found. Please create some events first.")
            return
        
        # Get all users
        users = User.query.all()
        if not users:
            print("❌ No users found. Please create some users first.")
            return
        
        print(f"📅 Found {len(events)} events")
        print(f"👥 Found {len(users)} users")
        
        # Clear existing feedback data
        Feedback.query.delete()
        db.session.commit()
        print("🗑️ Cleared existing feedback data")
        
        feedback_count = 0
        
        for event in events:
            # Skip cancelled events
            if event.status == 'cancelled':
                continue
            
            # Get users who have RSVP'd to this event
            rsvps = RSVP.query.filter_by(event_id=event.id, status='accepted').all()
            
            if not rsvps:
                print(f"⚠️ No accepted RSVPs for event: {event.name}")
                continue
            
            # Create feedback for 60-80% of attendees
            num_feedbacks = max(1, int(len(rsvps) * random.uniform(0.6, 0.8)))
            selected_rsvps = random.sample(rsvps, min(num_feedbacks, len(rsvps)))
            
            print(f"📝 Creating {len(selected_rsvps)} feedback entries for: {event.name}")
            
            for rsvp in selected_rsvps:
                # Generate realistic feedback ratings
                # Most events should have good ratings (3-5), with some variation
                base_rating = random.uniform(3.0, 4.5)
                
                # Add some variation to each category
                overall_rating = max(1, min(5, int(base_rating + random.uniform(-0.5, 0.5))))
                content_quality = max(1, min(5, int(base_rating + random.uniform(-0.7, 0.7))))
                organization = max(1, min(5, int(base_rating + random.uniform(-0.6, 0.6))))
                venue_rating = max(1, min(5, int(base_rating + random.uniform(-0.8, 0.8))))
                value_for_money = max(1, min(5, int(base_rating + random.uniform(-0.9, 0.9))))
                likelihood_to_recommend = max(1, min(5, int(base_rating + random.uniform(-0.5, 0.5))))
                
                # Generate realistic comments (30% chance)
                comments = None
                if random.random() < 0.3:
                    comments = generate_realistic_comment(overall_rating)
                
                # Create feedback
                feedback = Feedback(
                    event_id=event.id,
                    user_id=rsvp.user_id,
                    overall_rating=overall_rating,
                    content_quality=content_quality,
                    organization=organization,
                    venue_rating=venue_rating,
                    value_for_money=value_for_money,
                    likelihood_to_recommend=likelihood_to_recommend,
                    additional_comments=comments,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                
                db.session.add(feedback)
                feedback_count += 1
        
        # Commit all feedback
        db.session.commit()
        
        print(f"✅ Created {feedback_count} dummy feedback entries")
        print("\n🎯 Feedback Distribution:")
        
        # Show some statistics
        for event in events:
            if event.status == 'cancelled':
                continue
                
            feedbacks = Feedback.query.filter_by(event_id=event.id).all()
            if feedbacks:
                avg_overall = sum(f.overall_rating for f in feedbacks) / len(feedbacks)
                print(f"  📊 {event.name}: {len(feedbacks)} feedbacks, avg rating: {avg_overall:.1f}/5.0")
        
        print(f"\n🚀 You can now view the feedback analytics at: http://localhost:5001/admin/feedback-analytics")
        print("   (Make sure to login as an admin user)")

def generate_realistic_comment(rating):
    """Generate realistic comments based on rating"""
    positive_comments = [
        "Great event! The content was very informative and well-organized.",
        "Excellent presentation and good networking opportunities.",
        "Really enjoyed the event. The speaker was engaging and knowledgeable.",
        "Well worth attending. Learned a lot and met interesting people.",
        "Fantastic event! The venue was perfect and the content was top-notch.",
        "Very professional event. Everything was well-planned and executed.",
        "Amazing experience! Would definitely recommend to others.",
        "Great value for money. The event exceeded my expectations.",
        "Wonderful event with excellent speakers and great atmosphere.",
        "Really impressed with the quality and organization of this event."
    ]
    
    neutral_comments = [
        "Good event overall. Some areas could be improved but generally satisfied.",
        "Decent event. The content was okay but could have been more engaging.",
        "Average event. Nothing exceptional but not bad either.",
        "The event was fine. Met some interesting people but content was basic.",
        "Okay event. Some good points but room for improvement.",
        "Mixed experience. Some parts were good, others could be better.",
        "Fair event. The organization was decent but content could be stronger.",
        "Standard event. Nothing particularly memorable but not disappointing either."
    ]
    
    negative_comments = [
        "The event could have been better organized. Some technical issues occurred.",
        "Content was not as advertised. Expected more depth and quality.",
        "Venue was not ideal for this type of event. Poor acoustics.",
        "Event felt rushed and not well-planned. Could use better structure.",
        "Disappointed with the overall quality. Expected more for the price.",
        "The event had potential but execution was lacking.",
        "Not worth the time and money. Content was superficial.",
        "Poor organization and communication. Many attendees seemed confused."
    ]
    
    if rating >= 4:
        return random.choice(positive_comments)
    elif rating >= 3:
        return random.choice(neutral_comments)
    else:
        return random.choice(negative_comments)

if __name__ == "__main__":
    create_dummy_feedback()
