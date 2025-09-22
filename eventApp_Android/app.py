"""
Flask RSVP event application

This application implements comprehensive event management features including:
- User registration and authentication
- Event creation and management
- RSVP responses with guest tracking
- QR code generation and verification
- Email notifications
- Analytics and reporting
- Admin dashboard
- Security best practices

Designed for deployment on PythonAnywhere with minimal external dependencies.
"""

import base64
import io
import os
import uuid
import shutil
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for, jsonify, send_from_directory)
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

import qrcode

# Conditional Stripe import
try:
    import stripe
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
    stripe = None

# Load environment variables
try:
    load_dotenv()
except:
    pass  # Continue without .env file for local testing


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'replace-with-a-secure-random-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///eventapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL', 'noblequest.edu@outlook.com')

# Flask URL configuration (for email verification)
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME', '127.0.0.1:5001')
app.config['APPLICATION_ROOT'] = os.getenv('APPLICATION_ROOT', '/')
app.config['PREFERRED_URL_SCHEME'] = os.getenv('PREFERRED_URL_SCHEME', 'http')

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads/events'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Stripe configuration
app.config['STRIPE_PUBLISHABLE_KEY'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
app.config['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY')
app.config['STRIPE_WEBHOOK_SECRET'] = os.getenv('STRIPE_WEBHOOK_SECRET')

# Default Currency and Country Configuration
app.config['DEFAULT_CURRENCY'] = 'SGD'
app.config['DEFAULT_COUNTRY'] = 'Singapore'

# Superuser Configuration
app.config['SUPERUSER_PASSWORD'] = os.getenv('SUPERUSER_PASSWORD', 'TXGF#813193')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize Stripe (only if available and API key is provided)
if STRIPE_AVAILABLE and app.config.get('STRIPE_SECRET_KEY'):
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Language configuration
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh': '中文'
}

# Import translations from separate file
from translations import TRANSLATIONS

def get_current_language():
    """Get current language from session or user preference."""
    if current_user.is_authenticated and current_user.locale:
        return current_user.locale
    return session.get('language', 'en')

def get_translation(key, language=None):
    """Get translation for a key in the specified language."""
    if language is None:
        language = get_current_language()
    return TRANSLATIONS.get(language, TRANSLATIONS['en']).get(key, key)

# Make helper functions and config available to templates
@app.context_processor
def inject_helpers():
    return {
        'get_membership_grade_info': get_membership_grade_info,
        'get_currency_info': get_currency_info,
        'stripe_publishable_key': app.config.get('STRIPE_PUBLISHABLE_KEY', ''),
        'default_currency': app.config.get('DEFAULT_CURRENCY', 'SGD'),
        'default_country': app.config.get('DEFAULT_COUNTRY', 'Singapore'),
        'get_current_language': get_current_language,
        'get_translation': get_translation,
        'supported_languages': SUPPORTED_LANGUAGES
    }

# Membership grade configuration (for admin management)
MEMBERSHIP_GRADES = {
    'Pending Review': {
        'name': 'Pending Review',
        'icon': 'fas fa-clock',
        'color': '#ffc107',
        'description': 'Membership under review'
    },
    'Classic': {
        'name': 'Classic',
        'icon': 'fas fa-star',
        'color': '#6c757d',
        'description': 'Basic membership'
    },
    'Silver': {
        'name': 'Silver',
        'icon': 'fas fa-medal',
        'color': '#c0c0c0',
        'description': 'Silver membership'
    },
    'Gold': {
        'name': 'Gold',
        'icon': 'fas fa-trophy',
        'color': '#ffd700',
        'description': 'Gold membership'
    },
    'Platinum': {
        'name': 'Platinum',
        'icon': 'fas fa-crown',
        'color': '#e5e4e2',
        'description': 'Platinum membership'
    },
    'Diamond': {
        'name': 'Diamond',
        'icon': 'fas fa-gem',
        'color': '#b9f2ff',
        'description': 'Diamond membership'
    }
}

# Membership type configuration (for user registration)
MEMBERSHIP_TYPES = {
    'NA': {
        'name': 'NA',
        'icon': 'fas fa-user',
        'color': '#6c757d',
        'description': 'Not applicable'
    },
    '会员': {
        'name': '会员',
        'icon': 'fas fa-star',
        'color': '#28a745',
        'description': 'Member'
    },
    '家族': {
        'name': '家族',
        'icon': 'fas fa-users',
        'color': '#17a2b8',
        'description': 'Family'
    },
    '星光': {
        'name': '星光',
        'icon': 'fas fa-star',
        'color': '#ffc107',
        'description': 'Starlight'
    },
    '嫡传': {
        'name': '嫡传',
        'icon': 'fas fa-crown',
        'color': '#dc3545',
        'description': 'Direct lineage'
    }
}


class User(UserMixin, db.Model):
    """Represents a registered user.

    Attributes:
        id (int): primary key.
        first_name (str): user's first name.
        last_name (str): user's last name.
        username (str): display name.
        email (str): unique email address.
        password_hash (str): hashed password.
        phone (str): phone number (optional).
        timezone (str): user's timezone.
        locale (str): user's locale preference.
        country (str): user's country.
        city (str): user's city.
        avatar_url (str): URL to user's avatar image.
        is_admin (bool): True if user is an administrator/organiser.
        email_notifications (bool): Whether user wants email notifications.
        push_notifications (bool): Whether user wants push notifications.
        sms_notifications (bool): Whether user wants SMS notifications.
        time_format_24h (bool): Whether user prefers 24-hour time format.
        privacy_show_city (bool): Whether to show city in public profile.
        privacy_show_full_name (bool): Whether to show full name in public profile.
        account_status (str): Account status (active/suspended).
        email_verified (bool): Whether email is verified.
        created_at (datetime): Account creation timestamp.
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    country_code = db.Column(db.String(5), nullable=True)  # Country code like +65, +1, etc.
    timezone = db.Column(db.String(50), default='UTC')
    locale = db.Column(db.String(10), default='en')
    country = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    avatar_url = db.Column(db.String(200), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    time_format_24h = db.Column(db.Boolean, default=False)
    privacy_show_city = db.Column(db.Boolean, default=True)
    privacy_show_full_name = db.Column(db.Boolean, default=True)
    account_status = db.Column(db.String(20), default='active')
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), nullable=True)
    email_verification_sent_at = db.Column(db.DateTime, nullable=True)
    password_reset_token = db.Column(db.String(100), nullable=True)
    password_reset_sent_at = db.Column(db.DateTime, nullable=True)
    membership_type = db.Column(db.String(20), default='NA')  # NA, 会员, 家族, 星光, 嫡传
    membership_grade = db.Column(db.String(20), default='Pending Review')  # Classic, Silver, Gold, Platinum, Diamond
    credit_point = db.Column(db.Float, default=0.0)  # Credit points for event payments
    has_default_password = db.Column(db.Boolean, default=False)  # Track if user has default password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    events = db.relationship('Event', backref='creator', lazy=True)
    rsvps = db.relationship('RSVP', backref='attendee', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

    def set_password(self, password: str, is_default: bool = False) -> None:
        self.password_hash = generate_password_hash(password)
        if is_default:
            self.has_default_password = True

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    def reset_to_default_password(self, default_password: str = "Noble1319") -> str:
        """Reset user password to a default value and mark as default."""
        self.set_password(default_password, is_default=True)
        return default_password

    def validate_email(self) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None

    def generate_verification_token(self) -> str:
        """Generate a unique verification token."""
        import secrets
        self.email_verification_token = secrets.token_urlsafe(32)
        self.email_verification_sent_at = datetime.utcnow()
        return self.email_verification_token

    def verify_email(self, token: str) -> bool:
        """Verify email with token."""
        if self.email_verified:
            return True
        if self.email_verification_token == token:
            self.email_verified = True
            self.email_verification_token = None
            self.email_verification_sent_at = None
            return True
        return False

    def is_verification_token_expired(self) -> bool:
        """Check if verification token is expired (24 hours)."""
        if not self.email_verification_sent_at:
            return True
        return datetime.utcnow() - self.email_verification_sent_at > timedelta(hours=24)

    def generate_password_reset_token(self) -> str:
        """Generate a unique password reset token."""
        import secrets
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_sent_at = datetime.utcnow()
        return self.password_reset_token

    def is_password_reset_token_expired(self) -> bool:
        """Check if password reset token is expired (1 hour)."""
        if not self.password_reset_sent_at:
            return True
        return datetime.utcnow() - self.password_reset_sent_at > timedelta(hours=1)

    def clear_password_reset_token(self) -> None:
        """Clear password reset token."""
        self.password_reset_token = None
        self.password_reset_sent_at = None

    @property
    def full_name(self) -> str:
        """Return full name if available, otherwise username."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def display_name(self) -> str:
        """Return display name based on privacy settings."""
        if self.privacy_show_full_name and self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


class Event(db.Model):
    """Represents an event created by an organiser.

    Attributes:
        id (int): primary key.
        name (str): event name.
        description (str): event objective/description (markdown supported).
        start_date (datetime): event start date and time.
        end_date (datetime): event end date and time.
        timezone (str): event timezone.
        location (str): venue address or location.
        city (str): event city.
        country (str): event country.
        capacity (int): maximum number of attendees.
        creator_id (int): user ID of the organiser.
        rsvp_deadline (datetime): last date/time to RSVP.
        visibility (str): event visibility (public/private/unlisted).
        allow_plus_ones (bool): whether attendees can bring guests.
        waitlist_enabled (bool): whether waitlist is enabled.
        auto_approval (bool): whether RSVPs are auto-approved.
        cover_image_url (str): URL to event cover image.
        tags (str): comma-separated event tags.
        status (str): event status (active/cancelled/completed).
        created_at (datetime): creation timestamp.
        updated_at (datetime): last update timestamp.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    timezone = db.Column(db.String(50), default='UTC')
    location = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)  # None means unlimited
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rsvp_deadline = db.Column(db.DateTime, nullable=True)
    visibility = db.Column(db.String(20), default='public')  # public/private/unlisted
    allow_plus_ones = db.Column(db.Boolean, default=True)
    waitlist_enabled = db.Column(db.Boolean, default=False)
    auto_approval = db.Column(db.Boolean, default=True)
    cover_image_url = db.Column(db.String(200), nullable=True)
    tags = db.Column(db.String(200), nullable=True)  # comma-separated
    price = db.Column(db.Float, default=0.0)  # Event price in USD
    status = db.Column(db.String(20), default='active')  # active/cancelled/completed
    feedback_enabled = db.Column(db.Boolean, default=False)  # Whether feedback is enabled for this event
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rsvps = db.relationship('RSVP', backref='event', lazy=True)
    invitations = db.relationship('Invitation', backref='event', lazy=True)

    @property
    def accepted_count(self) -> int:
        """Return total number of accepted attendees including guest counts."""
        count = 0
        for rsvp in self.rsvps:
            if rsvp.status == 'Accepted':
                count += 1 + (rsvp.guests or 0)
        return count

    @property
    def maybe_count(self) -> int:
        return sum(1 for rsvp in self.rsvps if rsvp.status == 'Maybe')

    @property
    def declined_count(self) -> int:
        return sum(1 for rsvp in self.rsvps if rsvp.status == 'Declined')
    
    @property
    def is_past(self) -> bool:
        """Check if the event has already ended."""
        return self.start_date < datetime.utcnow()

    @property
    def waitlist_count(self) -> int:
        return sum(1 for rsvp in self.rsvps if rsvp.status == 'Waitlisted')

    @property
    def available_spots(self) -> int:
        if self.capacity is None:
            return float('inf')  # Unlimited capacity
        return max(self.capacity - self.accepted_count, 0)

    @property
    def is_full(self) -> bool:
        return self.capacity is not None and self.accepted_count >= self.capacity

    @property
    def is_past(self) -> bool:
        return self.start_date < datetime.utcnow()

    @property
    def is_upcoming(self) -> bool:
        return self.start_date > datetime.utcnow()

    @property
    def date(self) -> datetime:
        """Backward compatibility property."""
        return self.start_date


class RSVP(db.Model):
    """Represents an RSVP response from a user for an event.

    Attributes:
        id (int): primary key.
        event_id (int): associated event.
        user_id (int): associated user.
        status (str): 'Accepted', 'Maybe', 'Declined', or 'Waitlisted'.
        guests (int): number of additional guests.
        note (str): optional note from attendee.
        qr_code (str): unique code string for admission.
        checked_in (bool): whether user has been checked in.
        checked_in_at (datetime): when user was checked in.
        created_at (datetime): timestamp when RSVP was created.
        updated_at (datetime): timestamp when RSVP was last updated.
    """

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Accepted/Maybe/Declined/Waitlisted
    guests = db.Column(db.Integer, default=0)
    note = db.Column(db.Text, nullable=True)
    qr_code = db.Column(db.String(64), unique=True, nullable=True)
    checked_in = db.Column(db.Boolean, default=False)
    checked_in_at = db.Column(db.DateTime, nullable=True)
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    payment_amount = db.Column(db.Float, default=0.0)  # Amount paid in USD
    payment_method = db.Column(db.String(20), nullable=True)  # card, credit, free
    stripe_payment_intent_id = db.Column(db.String(200), nullable=True)  # Stripe payment intent ID
    receipt_url = db.Column(db.String(500), nullable=True)  # URL to receipt
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Invitation(db.Model):
    """Represents an invitation to an event.

    Attributes:
        id (int): primary key.
        event_id (int): associated event.
        email (str): invitee email address.
        user_id (int): associated user (if they have an account).
        token (str): unique invitation token.
        status (str): invitation status (pending/accepted/declined).
        personal_message (str): optional personal message from organizer.
        sent_at (datetime): when invitation was sent.
        responded_at (datetime): when invitee responded.
    """

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending/accepted/declined
    personal_message = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime, nullable=True)


class Notification(db.Model):
    """Represents an in-app notification for a user.

    Attributes:
        id (int): primary key.
        user_id (int): recipient user.
        type (str): notification type (invite/rsvp/event_update/etc).
        title (str): notification title.
        message (str): notification message.
        payload (str): JSON payload with additional data.
        read_at (datetime): when notification was read.
        created_at (datetime): when notification was created.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    payload = db.Column(db.Text, nullable=True)  # JSON data
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    """Represents user feedback for an event.
    
    Attributes:
        id (int): primary key.
        event_id (int): associated event.
        user_id (int): user who provided feedback.
        overall_rating (int): overall event rating (1-5 scale).
        content_quality (int): content quality rating (1-5 scale).
        organization (int): organization rating (1-5 scale).
        venue_rating (int): venue rating (1-5 scale).
        value_for_money (int): value for money rating (1-5 scale).
        likelihood_to_recommend (int): likelihood to recommend (1-5 scale).
        additional_comments (str): optional text feedback.
        created_at (datetime): when feedback was submitted.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Rating questions (1-5 scale)
    overall_rating = db.Column(db.Integer, nullable=False)
    content_quality = db.Column(db.Integer, nullable=False)
    organization = db.Column(db.Integer, nullable=False)
    venue_rating = db.Column(db.Integer, nullable=False)
    value_for_money = db.Column(db.Integer, nullable=False)
    likelihood_to_recommend = db.Column(db.Integer, nullable=False)
    
    # Optional text feedback
    additional_comments = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    event = db.relationship('Event', backref='feedbacks', lazy=True)
    user = db.relationship('User', backref='feedbacks', lazy=True)


class EventFeedbackForm(db.Model):
    """Represents a Microsoft Forms feedback form configuration for an event.
    
    Attributes:
        id (int): primary key.
        event_id (int): associated event.
        form_name (str): name/title of the feedback form.
        ms_form_id (str): Microsoft Forms form ID.
        ms_form_url (str): Microsoft Forms embed URL.
        is_active (bool): whether this form is currently active.
        created_by (int): user who created this form.
        created_at (datetime): when form was created.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    form_name = db.Column(db.String(200), nullable=False)
    ms_form_id = db.Column(db.String(100), nullable=False)  # MS Forms form ID
    ms_form_url = db.Column(db.Text, nullable=False)  # MS Forms embed URL
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    event = db.relationship('Event', backref='feedback_forms', lazy=True)
    creator = db.relationship('User', backref='created_feedback_forms', lazy=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    """Save uploaded file and return the filename."""
    if file and allowed_file(file.filename):
        # Create upload directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{uuid.uuid4()}{ext}"
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        return f"/static/uploads/events/{unique_filename}"
    return None


def send_email(to_email, subject, body, html_body=None):
    """Send email notification."""
    # Check if email is configured
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print(f"❌ Email not configured. Missing MAIL_USERNAME or MAIL_PASSWORD")
        print(f"   Would send to {to_email}: {subject}")
        print(f"   Please create a .env file with email configuration")
        return False
    
    try:
        print(f"📧 Attempting to send email to {to_email}...")
        print(f"   Server: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
        print(f"   Username: {app.config['MAIL_USERNAME']}")
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = app.config.get('ADMIN_EMAIL', app.config['MAIL_USERNAME'])
        msg['To'] = to_email
        
        # Add text and HTML parts
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Send email
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication failed: {e}")
        print(f"   Check your email credentials in .env file")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ Recipient refused: {e}")
        return False
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ SMTP Server disconnected: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False


def send_verification_email(user):
    """Send email verification link to user."""
    token = user.generate_verification_token()
    db.session.commit()
    
    verification_url = url_for('verify_email', token=token, _external=True)
    
    subject = "Verify Your Email Address - EventApp"
    
    text_body = f"""Hello {user.username},

Thank you for registering with EventApp! To complete your registration and start using your account, please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours for security reasons.

If you didn't create an account with EventApp, please ignore this email.

Best regards,
EventApp Team"""

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #007bff;">Welcome to EventApp!</h2>
            <p>Hello {user.username},</p>
            <p>Thank you for registering with EventApp! To complete your registration and start using your account, please verify your email address by clicking the button below:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}" 
                   style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Verify Email Address
                </a>
            </div>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 3px;">
                {verification_url}
            </p>
            
            <p><strong>Important:</strong> This link will expire in 24 hours for security reasons.</p>
            
            <p>If you didn't create an account with EventApp, please ignore this email.</p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="color: #666; font-size: 14px;">
                Best regards,<br>
                EventApp Team
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user.email, subject, text_body, html_body)


def send_password_reset_email(user):
    """Send password reset link to user."""
    token = user.generate_password_reset_token()
    db.session.commit()
    
    reset_url = url_for('reset_password', token=token, _external=True)
    
    subject = "Reset Your Password - EventApp"
    
    text_body = f"""Hello {user.username},

You requested to reset your password for your EventApp account. To reset your password, please click the link below:

{reset_url}

This link will expire in 1 hour for security reasons.

If you didn't request a password reset, please ignore this email. Your password will remain unchanged.

Best regards,
EventApp Team"""

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #dc3545;">Password Reset Request</h2>
            <p>Hello {user.username},</p>
            <p>You requested to reset your password for your EventApp account. To reset your password, please click the button below:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}" 
                   style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Reset Password
                </a>
            </div>
            
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 3px;">
                {reset_url}
            </p>
            
            <p><strong>Important:</strong> This link will expire in 1 hour for security reasons.</p>
            
            <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="color: #666; font-size: 14px;">
                Best regards,<br>
                EventApp Team
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user.email, subject, text_body, html_body)


def get_membership_grade_info(grade):
    """Get membership grade information."""
    return MEMBERSHIP_GRADES.get(grade, MEMBERSHIP_GRADES['Classic'])

def get_membership_type_info(membership_type):
    """Get membership type information."""
    return MEMBERSHIP_TYPES.get(membership_type, MEMBERSHIP_TYPES['NA'])

def get_currency_info(country='Singapore'):
    """Get currency information based on country."""
    currencies = {
        'Singapore': {
            'code': 'SGD',
            'symbol': 'S$',
            'name': 'Singapore Dollar',
            'phone_prefix': '+65',
            'phone_placeholder': '+65 9123 4567'
        },
        'Malaysia': {
            'code': 'MYR',
            'symbol': 'RM',
            'name': 'Malaysian Ringgit',
            'phone_prefix': '+60',
            'phone_placeholder': '+60 12-345 6789'
        }
    }
    return currencies.get(country, currencies['Singapore'])


def validate_superuser_password(password):
    """Validate superuser password."""
    return password == app.config['SUPERUSER_PASSWORD']


def create_stripe_payment_intent(amount, currency='sgd', metadata=None):
    """Create a Stripe payment intent."""
    if not STRIPE_AVAILABLE or not app.config.get('STRIPE_SECRET_KEY'):
        print("Stripe not available or configured - payment intent creation skipped")
        return None
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            metadata=metadata or {}
        )
        return intent
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None


def create_stripe_checkout_session(amount, event_name, rsvp_id, success_url, cancel_url, currency='sgd'):
    """Create a Stripe checkout session."""
    if not STRIPE_AVAILABLE or not app.config.get('STRIPE_SECRET_KEY'):
        print("Stripe not available or configured - checkout session creation skipped")
        return None
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': f'Event: {event_name}',
                    },
                    'unit_amount': int(amount * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'rsvp_id': str(rsvp_id),
                'event_name': event_name
            }
        )
        return session
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None


def create_notification(user_id, notification_type, title, message, payload=None):
    """Create an in-app notification."""
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message,
        payload=payload
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def create_feedback_notifications_for_event(event):
    """Create feedback notifications for all attendees when event starts."""
    # Get all users who RSVP'd to this event (any status)
    rsvps = RSVP.query.filter_by(event_id=event.id).all()
    
    for rsvp in rsvps:
        # Check if user has already submitted feedback
        existing_feedback = Feedback.query.filter_by(event_id=event.id, user_id=rsvp.user_id).first()
        if not existing_feedback:
            # Create feedback notification
            payload = {
                'event_id': event.id,
                'event_name': event.name,
                'event_date': event.start_date.isoformat() if event.start_date else None
            }
            
            create_notification(
                user_id=rsvp.user_id,
                notification_type='feedback_request',
                title='Event Feedback Request',
                message=f'How was "{event.name}"? Please share your feedback to help us improve future events.',
                payload=json.dumps(payload)
            )


def send_event_notification(event, notification_type, user=None):
    """Send event-related email notifications."""
    if not user:
        # Send to all attendees
        attendees = User.query.join(RSVP).filter(
            RSVP.event_id == event.id,
            RSVP.status == 'Accepted',
            User.email_notifications == True
        ).all()
    else:
        attendees = [user] if user.email_notifications else []
    
    for attendee in attendees:
        if notification_type == 'event_created':
            subject = f"New Event: {event.name}"
            body = f"""Hello {attendee.display_name},

A new event has been created:

Event: {event.name}
Date: {event.start_date.strftime('%Y-%m-%d %H:%M')}
Location: {event.location}
Description: {event.description}

Please RSVP at: {request.url_root}event/{event.id}

Best regards,
EventApp Team"""
        elif notification_type == 'event_updated':
            subject = f"Event Updated: {event.name}"
            body = f"""Hello {attendee.display_name},

The event "{event.name}" has been updated:

Date: {event.start_date.strftime('%Y-%m-%d %H:%M')}
Location: {event.location}
Description: {event.description}

Please check the updated details at: {request.url_root}event/{event.id}

Best regards,
EventApp Team"""
        elif notification_type == 'rsvp_confirmation':
            subject = f"RSVP Confirmation: {event.name}"
            body = f"""Hello {attendee.display_name},

Thank you for your RSVP to "{event.name}".

Event Details:
Date: {event.start_date.strftime('%Y-%m-%d %H:%M')}
Location: {event.location}

Your QR code for check-in is available at: {request.url_root}event/{event.id}

Best regards,
EventApp Team"""
        elif notification_type == 'waitlist_promotion':
            subject = f"You're In! {event.name}"
            body = f"""Hello {attendee.display_name},

Great news! You've been promoted from the waitlist for "{event.name}".

Event Details:
Date: {event.start_date.strftime('%Y-%m-%d %H:%M')}
Location: {event.location}

Your QR code for check-in is available at: {request.url_root}event/{event.id}

Best regards,
EventApp Team"""
        elif notification_type == 'event_cancelled':
            subject = f"Event Cancelled: {event.name}"
            body = f"""Hello {attendee.display_name},

We regret to inform you that the event "{event.name}" has been cancelled.

Event Details:
Date: {event.start_date.strftime('%Y-%m-%d %H:%M')}
Location: {event.location}

We apologize for any inconvenience this may cause. Please check our other upcoming events.

Best regards,
EventApp Team"""
        else:
            # Default case to prevent UnboundLocalError
            subject = f"Event Notification: {event.name}"
            body = f"""Hello {attendee.display_name},

This is a notification regarding the event "{event.name}".

Event Details:
Date: {event.start_date.strftime('%Y-%m-%d %H:%M')}
Location: {event.location}

Please visit: {request.url_root}event/{event.id}

Best regards,
EventApp Team"""
        
        send_email(attendee.email, subject, body)
        
        # Also create in-app notification
        create_notification(
            attendee.id,
            notification_type,
            subject,
            body.split('\n\n')[1] if '\n\n' in body else body
        )


def generate_qr_image(code: str) -> str:
    """Generate a QR code image as a base64 string for embedding in HTML.

    Args:
        code: Unique code to encode in the QR image.

    Returns:
        Base64 encoded PNG image string.
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_b64


def create_tables():
    db.create_all()
    
    # Add sample events with cover images if no events exist
    # Temporarily commented out to avoid database query during import
    # Will be re-enabled after database migration
    pass

# Create tables when app starts
with app.app_context():
    create_tables()


@app.before_request
def check_email_verification():
    """Check if logged-in user has verified their email."""
    if current_user.is_authenticated and not current_user.email_verified:
        # Allow users with default passwords to bypass email verification
        if current_user.has_default_password:
            # Skip email verification for users with default passwords
            pass
        else:
            # Allow access to verification-related routes
            if request.endpoint in ['verify_email', 'resend_verification', 'logout']:
                return
            # Redirect to verification page for other routes
            flash('Please verify your email address to continue using your account.', 'warning')
            return redirect(url_for('resend_verification'))
    
    # Check if user needs to change password
    if current_user.is_authenticated and session.get('force_password_change'):
        # Allow access to password change and logout routes
        if request.endpoint in ['change_password', 'logout']:
            return
        # Redirect to password change page for other routes
        flash('Please change your password to continue using your account.', 'warning')
        return redirect(url_for('change_password'))


@app.route('/')
def index():
    """Home page showing upcoming events."""
    events = Event.query.filter(Event.status != 'cancelled').order_by(Event.start_date.asc()).all()
    return render_template('index.html', events=events)

@app.route('/manifest.json')
def manifest():
    """Serve PWA manifest file"""
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

@app.route('/sw.js')
def service_worker():
    """Serve service worker file"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@app.route('/set_language/<language>')
def set_language(language):
    """Set the language preference."""
    if language in SUPPORTED_LANGUAGES:
        session['language'] = language
        # Update user's locale preference if logged in
        if current_user.is_authenticated:
            current_user.locale = language
            db.session.commit()
    return redirect(request.referrer or url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        country_code = request.form.get('country_code', '+65').strip()
        phone = request.form.get('phone', '').strip()
        membership_type = request.form.get('membership_type', 'NA').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        errors = []
        if not username or len(username) < 2:
            errors.append('Username must be at least 2 characters long.')
        if not email:
            errors.append('Email is required.')
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address.')
        if not phone:
            errors.append('Phone number is required.')
        elif not re.match(r'^[0-9]{7,15}$', phone.replace(' ', '').replace('-', '')):
            errors.append('Please enter a valid phone number (7-15 digits).')
        if not country_code:
            errors.append('Country code is required.')
        elif not re.match(r'^\+[1-9][0-9]{0,3}$', country_code):
            errors.append('Please enter a valid country code (e.g., +65, +1).')
        if not membership_type:
            errors.append('Membership type is required.')
        elif membership_type not in MEMBERSHIP_TYPES:
            errors.append('Please select a valid membership type.')
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, phone=phone, country_code=country_code, membership_type=membership_type, country='Singapore')
        user.set_password(password)
        user.email_verified = False  # Require email verification
        db.session.add(user)
        db.session.commit()
        
        # Send verification email
        if send_verification_email(user):
            flash('Registration successful! Please check your email to verify your account before logging in.', 'success')
        else:
            flash('Registration successful, but failed to send verification email. Please contact support.', 'warning')
        
        return redirect(url_for('resend_verification'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Check if user has default password - allow login without email verification
            if user.has_default_password:
                flash('Your password has been reset by an administrator. Please change your password for security.', 'warning')
                session['force_password_change'] = True
                session['user_id_for_password_change'] = user.id
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            
            # Check if email is verified (only for users without default passwords)
            if not user.email_verified:
                flash('Please verify your email address before logging in. Check your email for a verification link.', 'warning')
                return redirect(url_for('resend_verification'))
            
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password for users with default passwords."""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not current_password or not new_password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'danger')
            return render_template('change_password.html')
        
        # Verify current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return render_template('change_password.html')
        
        # Update password
        current_user.set_password(new_password, is_default=False)
        current_user.has_default_password = False
        
        # If user had a default password, also verify their email
        if session.get('force_password_change'):
            current_user.email_verified = True
        
        db.session.commit()
        
        # Clear the force password change session
        session.pop('force_password_change', None)
        session.pop('user_id_for_password_change', None)
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('change_password.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/verify-email/<token>')
def verify_email(token):
    """Verify user email with token."""
    user = User.query.filter_by(email_verification_token=token).first()
    
    if not user:
        flash('Invalid or expired verification link.', 'danger')
        return redirect(url_for('index'))
    
    if user.is_verification_token_expired():
        flash('Verification link has expired. Please request a new one.', 'danger')
        return redirect(url_for('resend_verification'))
    
    if user.verify_email(token):
        db.session.commit()
        flash('Email verified successfully! You can now use your account.', 'success')
        return redirect(url_for('login'))
    else:
        flash('Email verification failed.', 'danger')
        return redirect(url_for('index'))


@app.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    """Resend email verification."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Email is required.', 'danger')
            return render_template('resend_verification.html')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('No account found with that email address.', 'danger')
            return render_template('resend_verification.html')
        
        if user.email_verified:
            flash('Email is already verified. You can log in.', 'info')
            return redirect(url_for('login'))
        
        # Send verification email
        if send_verification_email(user):
            flash('Verification email sent! Please check your email and click the verification link.', 'success')
        else:
            flash('Failed to send verification email. Please check your email configuration or try again later.', 'danger')
        
        return render_template('resend_verification.html')
    
    return render_template('resend_verification.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Email is required.', 'danger')
            return render_template('forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        # Always show success message for security (don't reveal if email exists)
        if user:
            if send_password_reset_email(user):
                flash('If an account with that email exists, a password reset link has been sent.', 'success')
            else:
                flash('Failed to send password reset email. Please check your email configuration or try again later.', 'danger')
        else:
            flash('If an account with that email exists, a password reset link has been sent.', 'success')
        
        return render_template('forgot_password.html')
    
    return render_template('forgot_password.html')


# Admin password reset route (must be before general reset-password route)
@app.route('/admin/members/<int:user_id>/reset-password', methods=['POST'])
@login_required
def reset_member_password(user_id):
    """Reset a member's password to default (admin only with superuser password)."""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin_members'))
    
    user = User.query.get_or_404(user_id)
    superuser_password = request.form.get('superuser_password')
    
    if not validate_superuser_password(superuser_password):
        flash('Invalid superuser password.', 'danger')
        return redirect(url_for('admin_members'))
    
    # Generate a default password
    default_password = user.reset_to_default_password()
    db.session.commit()
    
    flash(f'Password reset successfully for {user.username}. Default password: {default_password}. Please share this with the user via email or WhatsApp.', 'success')
    return redirect(url_for('admin_members'))


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.query.filter_by(password_reset_token=token).first()
    
    if not user:
        flash('Invalid or expired password reset link.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if user.is_password_reset_token_expired():
        flash('Password reset link has expired. Please request a new one.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('reset_password.html', token=token)
        
        # Update password
        user.set_password(password)
        user.clear_password_reset_token()
        db.session.commit()
        
        flash('Password reset successfully! You can now log in with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)


@app.route('/event/new', methods=['GET', 'POST'])
@login_required
def create_event():
    """Create a new event (admin/organiser only)."""
    if not current_user.is_admin:
        flash('Only organisers can create events.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        date_str = request.form.get('date')  # format: YYYY-MM-DD
        time_str = request.form.get('time')  # format: HH:MM
        end_time_str = request.form.get('end_time')  # format: HH:MM
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        price = request.form.get('price', 0)  # Event price
        rsvp_deadline_str = request.form.get('rsvp_deadline')  # optional
        
        # Handle image upload
        cover_image_url = None
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file.filename:  # If file is selected
                cover_image_url = save_uploaded_file(file)
                if not cover_image_url:
                    flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP images.', 'danger')
                    return redirect(url_for('create_event'))
        
        try:
            event_datetime = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        except (ValueError, TypeError):
            flash('Invalid start date or time.', 'danger')
            return redirect(url_for('create_event'))
        
        # Handle end time
        end_datetime = None
        if end_time_str:
            try:
                end_datetime = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')
                if end_datetime <= event_datetime:
                    flash('End time must be after start time.', 'danger')
                    return redirect(url_for('create_event'))
            except (ValueError, TypeError):
                flash('Invalid end time.', 'danger')
                return redirect(url_for('create_event'))
        
        try:
            capacity_int = int(capacity)
        except (ValueError, TypeError):
            flash('Capacity must be a number.', 'danger')
            return redirect(url_for('create_event'))
        
        try:
            price_float = float(price)
            if price_float < 0:
                flash('Price cannot be negative.', 'danger')
                return redirect(url_for('create_event'))
        except (ValueError, TypeError):
            flash('Price must be a valid number.', 'danger')
            return redirect(url_for('create_event'))
        
        rsvp_deadline = None
        if rsvp_deadline_str:
            try:
                rsvp_deadline = datetime.strptime(rsvp_deadline_str, '%Y-%m-%d %H:%M')
            except (ValueError, TypeError):
                flash('Invalid RSVP deadline.', 'danger')
                return redirect(url_for('create_event'))
        
        event = Event(name=name,
                      description=description,
                      start_date=event_datetime,
                      end_date=end_datetime,
                      location=location,
                      capacity=capacity_int,
                      price=price_float,
                      creator=current_user,
                      rsvp_deadline=rsvp_deadline,
                      cover_image_url=cover_image_url)
        db.session.add(event)
        db.session.commit()
        
        # Send notifications to all users (optional - you might want to limit this)
        # send_event_notification(event, 'event_created')
        
        flash('Event created successfully.', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    return render_template('create_event.html')


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_detail(event_id):
    """View event details and handle RSVP responses."""
    event = Event.query.get_or_404(event_id)
    
    # Check if event is cancelled
    if event.status == 'cancelled':
        flash('This event has been cancelled and is no longer available.', 'warning')
        return redirect(url_for('index'))
    
    rsvp = RSVP.query.filter_by(event_id=event.id, user_id=current_user.id).first()
    if request.method == 'POST':
        # Handle RSVP submission with integrated payment
        status = request.form.get('status')
        guests = request.form.get('guests') or 0
        payment_method = request.form.get('payment_method')
        
        try:
            guests_int = int(guests)
            if guests_int < 0:
                raise ValueError
        except ValueError:
            flash('Guests must be a non‑negative integer.', 'danger')
            return redirect(url_for('event_detail', event_id=event.id))
        
        # Check capacity
        total_attending = event.accepted_count
        new_total = total_attending + (1 + guests_int if status == 'Accepted' else 0)
        if status == 'Accepted' and new_total > event.capacity:
            flash('Event capacity reached. You can no longer accept.', 'danger')
            return redirect(url_for('event_detail', event_id=event.id))
        
        if rsvp is None:
            rsvp = RSVP(event_id=event.id, user_id=current_user.id)
            db.session.add(rsvp)
        
        # Update RSVP details
        rsvp.status = status
        rsvp.guests = guests_int
        
        # Handle payment for accepted RSVPs
        if status == 'Accepted':
            if event.price > 0:
                if not payment_method:
                    flash('Please select a payment method for this paid event.', 'danger')
                    return redirect(url_for('event_detail', event_id=event.id))
                
                if payment_method == 'credit':
                    # Check if user has sufficient credits
                    if (current_user.credit_point or 0) < event.price:
                        flash('Insufficient credits. You need {:.2f} more credits.'.format(event.price - (current_user.credit_point or 0)), 'danger')
                        return redirect(url_for('event_detail', event_id=event.id))
                    
                    # Deduct credits and mark as paid
                    current_user.credit_point = (current_user.credit_point or 0) - event.price
                    rsvp.payment_status = 'paid'
                    rsvp.payment_amount = event.price
                    rsvp.payment_method = 'credit'
                    flash('Payment successful! Credits deducted from your account.', 'success')
                
                elif payment_method == 'card':
                    # Redirect to Stripe payment
                    rsvp.payment_method = 'card'
                    db.session.commit()
                    return redirect(url_for('create_payment', event_id=event.id))
            else:
                # Free event
                rsvp.payment_status = 'paid'
                rsvp.payment_amount = 0.0
                rsvp.payment_method = 'free'
            
            # Generate unique QR code if accepted
            if not rsvp.qr_code:
                code = str(uuid.uuid4())
                # Ensure uniqueness across RSVPs
                while RSVP.query.filter_by(qr_code=code).first():
                    code = str(uuid.uuid4())
                rsvp.qr_code = code
            
            # Send confirmation email
            send_event_notification(event, 'rsvp_confirmation', current_user)
        else:
            # Clear payment and QR code if not attending
            rsvp.qr_code = None
            rsvp.payment_status = 'pending'
            rsvp.payment_amount = 0.0
            rsvp.payment_method = None
        
        db.session.commit()
        flash('Your RSVP has been updated.', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    qr_image = None
    if rsvp and rsvp.qr_code:
        qr_image = generate_qr_image(rsvp.qr_code)
    return render_template('event_detail.html', event=event, rsvp=rsvp, qr_image=qr_image)


@app.route('/verify', methods=['GET', 'POST'])
@login_required
def verify_qr():
    """Page for organisers to verify a QR code and check‑in attendees."""
    if not current_user.is_admin:
        flash('Only organisers can verify attendees.', 'danger')
        return redirect(url_for('index'))
    attendee = None
    if request.method == 'POST':
        code = request.form.get('code')
        rsvp = RSVP.query.filter_by(qr_code=code).first()
        if not rsvp:
            flash('QR code not found.', 'danger')
        else:
            if rsvp.checked_in:
                flash('Attendee already checked in.', 'warning')
                attendee = rsvp
            else:
                rsvp.checked_in = True
                rsvp.checked_in_at = datetime.utcnow()  # Record check-in timestamp
                db.session.commit()
                flash('Check‑in successful.', 'success')
                attendee = rsvp
    return render_template('verify.html', attendee=attendee)


@app.route('/dashboard')
@login_required
def dashboard():
    """Organiser dashboard showing events and RSVP stats."""
    if not current_user.is_admin:
        flash('Only organisers can view the dashboard.', 'danger')
        return redirect(url_for('index'))
    events = Event.query.filter_by(creator_id=current_user.id).filter(Event.status != 'cancelled').order_by(Event.start_date.desc()).all()
    return render_template('dashboard.html', events=events)


@app.route('/my-events')
@login_required
def my_events():
    """Shows events the user has RSVP'd to."""
    rsvps = RSVP.query.join(Event).options(
        db.joinedload(RSVP.event).joinedload(Event.feedbacks)
    ).filter(
        RSVP.user_id == current_user.id,
        Event.status != 'cancelled'
    ).all()
    return render_template('my_events.html', rsvps=rsvps)


@app.route('/event/<int:event_id>/update', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    """Update an existing event (organiser only)."""
    event = Event.query.get_or_404(event_id)
    
    # Check if event is cancelled
    if event.status == 'cancelled':
        flash('Cannot update a cancelled event.', 'warning')
        return redirect(url_for('index'))
    
    if current_user.id != event.creator_id and not current_user.is_admin:
        flash('You do not have permission to update this event.', 'danger')
        return redirect(url_for('event_detail', event_id=event.id))
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        end_time_str = request.form.get('end_time')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        price = request.form.get('price', 0)  # Event price
        rsvp_deadline_str = request.form.get('rsvp_deadline')
        feedback_enabled = request.form.get('feedback_enabled') == 'on'  # Checkbox value
        
        # Handle image upload
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file.filename:  # If file is selected
                cover_image_url = save_uploaded_file(file)
                if not cover_image_url:
                    flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP images.', 'danger')
                    return redirect(url_for('update_event', event_id=event.id))
                event.cover_image_url = cover_image_url
        
        try:
            event_datetime = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        except (ValueError, TypeError):
            flash('Invalid start date or time.', 'danger')
            return redirect(url_for('update_event', event_id=event.id))
        
        # Handle end time
        end_datetime = None
        if end_time_str:
            try:
                end_datetime = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')
                if end_datetime <= event_datetime:
                    flash('End time must be after start time.', 'danger')
                    return redirect(url_for('update_event', event_id=event.id))
            except (ValueError, TypeError):
                flash('Invalid end time.', 'danger')
                return redirect(url_for('update_event', event_id=event.id))
        
        try:
            capacity_int = int(capacity)
        except (ValueError, TypeError):
            flash('Capacity must be a number.', 'danger')
            return redirect(url_for('update_event', event_id=event.id))
        
        # Validate and convert price
        try:
            price_float = float(price)
            if price_float < 0:
                flash('Price cannot be negative.', 'danger')
                return redirect(url_for('update_event', event_id=event.id))
        except (ValueError, TypeError):
            flash('Price must be a valid number.', 'danger')
            return redirect(url_for('update_event', event_id=event.id))
        
        rsvp_deadline = None
        if rsvp_deadline_str:
            try:
                rsvp_deadline = datetime.strptime(rsvp_deadline_str, '%Y-%m-%d %H:%M')
            except (ValueError, TypeError):
                flash('Invalid RSVP deadline.', 'danger')
                return redirect(url_for('update_event', event_id=event.id))
        
        event.name = name
        event.description = description
        event.start_date = event_datetime
        event.end_date = end_datetime
        event.location = location
        event.capacity = capacity_int
        event.price = price_float
        event.rsvp_deadline = rsvp_deadline
        # Check if feedback was just enabled
        feedback_just_enabled = not event.feedback_enabled and feedback_enabled
        event.feedback_enabled = feedback_enabled
        db.session.commit()
        
        # Send notifications to attendees about update
        send_event_notification(event, 'event_updated')
        
        # If feedback was just enabled, send feedback notifications to all attendees
        if feedback_just_enabled:
            create_feedback_notifications_for_event(event)
        
        flash('Event updated successfully.', 'success')
        return redirect(url_for('event_detail', event_id=event.id))
    # Prepopulate form with current values
    return render_template('update_event.html', event=event)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management."""
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        country = request.form.get('country', '').strip()
        city = request.form.get('city', '').strip()
        email_notifications = request.form.get('email_notifications') == 'on'
        push_notifications = request.form.get('push_notifications') == 'on'
        time_format_24h = request.form.get('time_format_24h') == 'on'
        privacy_show_city = request.form.get('privacy_show_city') == 'on'
        privacy_show_full_name = request.form.get('privacy_show_full_name') == 'on'
        
        # Validation
        if not username or len(username) < 2:
            flash('Username must be at least 2 characters long.', 'danger')
            return redirect(url_for('profile'))
        
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('profile'))
        
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Email already registered by another user.', 'danger')
            return redirect(url_for('profile'))
        
        # Update user fields
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.username = username
        current_user.email = email
        current_user.phone = phone
        current_user.country = country
        current_user.city = city
        current_user.email_notifications = email_notifications
        current_user.push_notifications = push_notifications
        current_user.time_format_24h = time_format_24h
        current_user.privacy_show_city = privacy_show_city
        current_user.privacy_show_full_name = privacy_show_full_name
        
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html')


@app.route('/analytics')
@login_required
def analytics():
    """Event analytics for organizers."""
    if not current_user.is_admin:
        flash('Only organizers can view analytics.', 'danger')
        return redirect(url_for('index'))
    
    # Get statistics
    total_events = Event.query.filter_by(creator_id=current_user.id).count()
    total_rsvps = db.session.query(RSVP).join(Event).filter(Event.creator_id == current_user.id).count()
    total_attendees = db.session.query(RSVP).join(Event).filter(
        Event.creator_id == current_user.id,
        RSVP.status == 'Accepted'
    ).count()
    
    # Recent events with stats
    recent_events = Event.query.filter_by(creator_id=current_user.id).order_by(Event.start_date.desc()).limit(5).all()
    
    return render_template('analytics.html', 
                         total_events=total_events,
                         total_rsvps=total_rsvps,
                         total_attendees=total_attendees,
                         recent_events=recent_events)


@app.route('/admin/members')
@login_required
def admin_members():
    """Admin member management page."""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    # Get all users with their details
    members = User.query.all()
    
    # Get membership grade statistics
    grade_stats = {}
    for grade in MEMBERSHIP_GRADES.keys():
        grade_stats[grade] = len([m for m in members if m.membership_grade == grade])
    
    return render_template('admin_members.html', members=members, grade_stats=grade_stats, get_membership_type_info=get_membership_type_info, MEMBERSHIP_TYPES=MEMBERSHIP_TYPES)


@app.route('/admin/members/export')
@login_required
def export_members():
    """Export all member data to CSV (admin only)."""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    import csv
    import io
    from flask import make_response
    
    # Get all users
    members = User.query.all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header row
    headers = [
        'ID', 'Username', 'First Name', 'Last Name', 'Email', 'Phone', 
        'Country', 'City', 'Timezone', 'Locale', 'Membership Type', 'Membership Grade',
        'Credit Points', 'Account Status', 'Email Verified', 'Is Admin',
        'Email Notifications', 'Push Notifications', 'SMS Notifications',
        'Time Format 24h', 'Privacy Show City', 'Privacy Show Full Name',
        'Has Default Password', 'Created At'
    ]
    writer.writerow(headers)
    
    # Write member data
    for member in members:
        row = [
            member.id,
            member.username,
            member.first_name or '',
            member.last_name or '',
            member.email,
            member.phone or '',
            member.country or '',
            member.city or '',
            member.timezone or '',
            member.locale or '',
            member.membership_type or '',
            member.membership_grade or '',
            member.credit_point or 0.0,
            member.account_status or '',
            'Yes' if member.email_verified else 'No',
            'Yes' if member.is_admin else 'No',
            'Yes' if member.email_notifications else 'No',
            'Yes' if member.push_notifications else 'No',
            'Yes' if member.sms_notifications else 'No',
            'Yes' if member.time_format_24h else 'No',
            'Yes' if member.privacy_show_city else 'No',
            'Yes' if member.privacy_show_full_name else 'No',
            'Yes' if member.has_default_password else 'No',
            member.created_at.strftime('%Y-%m-%d %H:%M:%S') if member.created_at else ''
        ]
        writer.writerow(row)
    
    # Prepare response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=members_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response


@app.route('/admin/members/<int:user_id>/update_grade', methods=['POST'])
@login_required
def update_member_grade(user_id):
    """Update a member's grade (admin only)."""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    new_grade = request.form.get('membership_grade')
    
    if new_grade not in MEMBERSHIP_GRADES:
        flash('Invalid membership grade.', 'danger')
        return redirect(url_for('admin_members'))
    
    old_grade = user.membership_grade
    user.membership_grade = new_grade
    db.session.commit()
    
    flash(f'Updated {user.username}\'s membership grade from {old_grade} to {new_grade}.', 'success')
    return redirect(url_for('admin_members'))


@app.route('/admin/validate-superuser', methods=['POST'])
@login_required
def validate_superuser():
    """Validate superuser password for sensitive operations."""
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'})
    
    password = request.form.get('password')
    action = request.form.get('action')
    member_id = request.form.get('member_id')
    
    if not validate_superuser_password(password):
        return jsonify({'success': False, 'error': 'Invalid superuser password'})
    
    # If it's an edit action, process the form data
    if action == 'edit_member' and member_id:
        form_data = request.form.get('form_data')
        if form_data:
            # Parse form data and update user
            user = User.query.get_or_404(int(member_id))
            
            # Parse the form data
            from urllib.parse import parse_qs
            parsed_data = parse_qs(form_data)
            
            # Update user fields
            user.username = parsed_data.get('username', [user.username])[0]
            user.email = parsed_data.get('email', [user.email])[0]
            user.first_name = parsed_data.get('first_name', [user.first_name])[0] or None
            user.last_name = parsed_data.get('last_name', [user.last_name])[0] or None
            user.phone = parsed_data.get('phone', [user.phone])[0] or None
            user.country = parsed_data.get('country', [user.country])[0] or None
            user.city = parsed_data.get('city', [user.city])[0] or None
            user.membership_grade = parsed_data.get('membership_grade', [user.membership_grade])[0]
            user.membership_type = parsed_data.get('membership_type', [user.membership_type])[0]
            user.account_status = parsed_data.get('account_status', [user.account_status])[0]
            user.is_admin = 'is_admin' in parsed_data
            user.email_verified = 'email_verified' in parsed_data
            
            # Update credit points
            credit_point = parsed_data.get('credit_point', [None])[0]
            if credit_point is not None:
                try:
                    user.credit_point = float(credit_point)
                    if user.credit_point < 0:
                        user.credit_point = 0.0
                except (ValueError, TypeError):
                    # Keep existing credit_point if invalid
                    pass
            
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Member updated successfully'})
    
    # If it's a password reset action, just validate the password
    if action == 'reset_password':
        return jsonify({'success': True, 'message': 'Password reset authorized'})
    
    return jsonify({'success': True})


@app.route('/admin/members/<int:user_id>/update', methods=['POST'])
@login_required
def update_member(user_id):
    """Update member details (admin only with superuser password)."""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    superuser_password = request.form.get('superuser_password')
    
    if not validate_superuser_password(superuser_password):
        flash('Invalid superuser password.', 'danger')
        return redirect(url_for('admin_members'))
    
    # Update user fields
    user.username = request.form.get('username', user.username)
    user.email = request.form.get('email', user.email)
    user.first_name = request.form.get('first_name') or None
    user.last_name = request.form.get('last_name') or None
    user.phone = request.form.get('phone') or None
    user.country = request.form.get('country') or None
    user.city = request.form.get('city') or None
    user.membership_grade = request.form.get('membership_grade', user.membership_grade)
    user.membership_type = request.form.get('membership_type', user.membership_type)
    user.account_status = request.form.get('account_status', user.account_status)
    user.is_admin = request.form.get('is_admin') == 'on'
    user.email_verified = request.form.get('email_verified') == 'on'
    
    # Update credit points (only superuser can modify)
    credit_point = request.form.get('credit_point')
    if credit_point is not None:
        try:
            user.credit_point = float(credit_point)
            if user.credit_point < 0:
                user.credit_point = 0.0
        except (ValueError, TypeError):
            flash('Invalid credit point value.', 'warning')
            user.credit_point = user.credit_point or 0.0
    
    db.session.commit()
    
    flash(f'Successfully updated {user.username}\'s details.', 'success')
    return redirect(url_for('admin_members'))


@app.route('/admin/members/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_member(user_id):
    """Delete a member (admin only with superuser password)."""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # For GET requests, show confirmation page
    if request.method == 'GET':
        return render_template('delete_member_confirm.html', user=user)
    
    # For POST requests, process deletion
    superuser_password = request.form.get('superuser_password')
    
    if not validate_superuser_password(superuser_password):
        flash('Invalid superuser password.', 'danger')
        return redirect(url_for('admin_members'))
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin_members'))
    
    username = user.username
    
    # Delete all related data
    # Delete RSVPs
    RSVP.query.filter_by(user_id=user_id).delete()
    
    # Delete notifications
    Notification.query.filter_by(user_id=user_id).delete()
    
    # Delete feedback
    Feedback.query.filter_by(user_id=user_id).delete()
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Successfully deleted member {username} and all associated data.', 'success')
    return redirect(url_for('admin_members'))


@app.route('/test-buttons')
def test_buttons():
    """Test page for debugging button functionality."""
    return send_from_directory('templates', 'test_buttons.html')

@app.route('/debug-buttons')
def debug_buttons():
    """Debug page for testing button functionality."""
    return send_from_directory('templates', 'debug_buttons.html')

@app.route('/simple-test')
def simple_test():
    """Simple test page for basic functionality."""
    return send_from_directory('templates', 'simple_test.html')


@app.route('/past-events')
@login_required
def past_events():
    """View past events."""
    # Get past events for current user (both organized and attended)
    organized_events = Event.query.filter(
        Event.creator_id == current_user.id,
        Event.start_date < datetime.utcnow(),
        Event.status != 'cancelled'
    ).order_by(Event.start_date.desc()).all()
    
    attended_events = Event.query.join(RSVP).filter(
        RSVP.user_id == current_user.id,
        Event.start_date < datetime.utcnow(),
        Event.status != 'cancelled'
    ).order_by(Event.start_date.desc()).all()
    
    # Combine and deduplicate
    all_past_events = list(set(organized_events + attended_events))
    all_past_events.sort(key=lambda x: x.start_date, reverse=True)
    
    return render_template('past_events.html', events=all_past_events)


@app.route('/notifications')
@login_required
def notifications():
    """View notifications."""
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    unread_count = Notification.query.filter_by(user_id=current_user.id, read_at=None).count()
    
    return render_template('notifications.html', notifications=user_notifications, unread_count=unread_count)


@app.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read."""
    notification = Notification.query.filter_by(id=notification_id, user_id=current_user.id).first_or_404()
    notification.read_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})


@app.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """Mark all notifications as read."""
    Notification.query.filter_by(user_id=current_user.id, read_at=None).update({'read_at': datetime.utcnow()})
    db.session.commit()
    return jsonify({'success': True})


@app.route('/event/<int:event_id>/feedback-form')
@login_required
def event_feedback_form(event_id):
    """Get feedback form for modal."""
    event = Event.query.get_or_404(event_id)
    
    # Check if event is cancelled
    if event.status == 'cancelled':
        return '<div class="alert alert-warning">Cannot provide feedback for a cancelled event.</div>'
    
    # Check if user has already submitted feedback
    existing_feedback = Feedback.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if existing_feedback:
        return '<div class="alert alert-info">You have already submitted feedback for this event.</div>'
    
    # Check if user has RSVP'd to this event (any status)
    rsvp = RSVP.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if not rsvp:
        return '<div class="alert alert-warning">You can only provide feedback for events you have RSVP\'d to.</div>'
    
    return render_template('feedback_form.html', event=event)

@app.route('/feedback/<int:event_id>')
@login_required
def feedback_page(event_id):
    """Dedicated feedback page for users with MS Forms."""
    event = Event.query.get_or_404(event_id)
    
    # Check if event is cancelled
    if event.status == 'cancelled':
        flash('Cannot provide feedback for a cancelled event.', 'warning')
        return redirect(url_for('index'))
    
    # Check if feedback is enabled for this event
    if not event.feedback_enabled:
        flash('Feedback is not enabled for this event.', 'warning')
        return redirect(url_for('index'))
    
    # Check if user has RSVP'd to this event (any status)
    rsvp = RSVP.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if not rsvp:
        flash('You can only provide feedback for events you have RSVP\'d to.', 'warning')
        return redirect(url_for('index'))
    
    # Get active feedback forms for this event
    feedback_forms = EventFeedbackForm.query.filter_by(event_id=event_id, is_active=True).all()
    
    if not feedback_forms:
        flash('No feedback forms are available for this event.', 'warning')
        return redirect(url_for('index'))
    
    return render_template('feedback_page_msforms.html', event=event, feedback_forms=feedback_forms)

@app.route('/event/<int:event_id>/feedback', methods=['GET', 'POST'])
@login_required
def event_feedback(event_id):
    """Redirect to MS Forms feedback page."""
    return redirect(url_for('feedback_page', event_id=event_id))


@app.route('/admin/event/<int:event_id>/send-feedback-notifications', methods=['POST'])
@login_required
def send_feedback_notifications(event_id):
    """Send feedback notifications for an event (admin only)."""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    event = Event.query.get_or_404(event_id)
    
    # Create feedback notifications for all attendees
    create_feedback_notifications_for_event(event)
    
    flash(f'Feedback notifications sent to all attendees of "{event.name}".', 'success')
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/admin/feedback-analytics')
@login_required
def feedback_analytics():
    """Admin feedback analytics page with Microsoft Forms."""
    if not current_user.is_admin:
        flash('Only administrators can view feedback analytics.', 'danger')
        return redirect(url_for('index'))
    
    # Get all events with their feedback forms
    events = Event.query.filter(Event.status != 'cancelled').order_by(Event.start_date.desc()).all()
    
    # Get feedback forms for each event
    event_forms = []
    for event in events:
        feedback_forms = EventFeedbackForm.query.filter_by(event_id=event.id, is_active=True).all()
        event_forms.append({
            'event': event,
            'feedback_forms': feedback_forms
        })
    
    return render_template('feedback_analytics.html', event_forms=event_forms)


@app.route('/admin/feedback-forms/add', methods=['GET', 'POST'])
@login_required
def add_feedback_form():
    """Add a new Microsoft Forms feedback form for an event."""
    if not current_user.is_admin:
        flash('Only administrators can manage feedback forms.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        form_name = request.form.get('form_name', '').strip()
        ms_form_id = request.form.get('ms_form_id', '').strip()
        ms_form_url = request.form.get('ms_form_url', '').strip()
        
        # Validation
        if not event_id or not form_name or not ms_form_id or not ms_form_url:
            flash('All fields are required.', 'danger')
            return redirect(url_for('add_feedback_form'))
        
        # Validate event exists
        event = Event.query.get(event_id)
        if not event:
            flash('Event not found.', 'danger')
            return redirect(url_for('add_feedback_form'))
        
        # Create new feedback form
        feedback_form = EventFeedbackForm(
            event_id=event_id,
            form_name=form_name,
            ms_form_id=ms_form_id,
            ms_form_url=ms_form_url,
            created_by=current_user.id
        )
        
        db.session.add(feedback_form)
        db.session.commit()
        
        flash(f'Feedback form "{form_name}" added successfully for event "{event.name}".', 'success')
        return redirect(url_for('feedback_analytics'))
    
    # GET request - show form
    events = Event.query.filter(Event.status != 'cancelled').order_by(Event.start_date.desc()).all()
    return render_template('add_feedback_form.html', events=events)


@app.route('/admin/feedback-forms/<int:form_id>/toggle', methods=['POST'])
@login_required
def toggle_feedback_form(form_id):
    """Toggle feedback form active status."""
    if not current_user.is_admin:
        flash('Only administrators can manage feedback forms.', 'danger')
        return redirect(url_for('index'))
    
    feedback_form = EventFeedbackForm.query.get_or_404(form_id)
    feedback_form.is_active = not feedback_form.is_active
    db.session.commit()
    
    status = 'activated' if feedback_form.is_active else 'deactivated'
    flash(f'Feedback form "{feedback_form.form_name}" {status}.', 'success')
    return redirect(url_for('feedback_analytics'))


@app.route('/admin/feedback-forms/<int:form_id>/delete', methods=['POST'])
@login_required
def delete_feedback_form(form_id):
    """Delete a feedback form."""
    if not current_user.is_admin:
        flash('Only administrators can manage feedback forms.', 'danger')
        return redirect(url_for('index'))
    
    feedback_form = EventFeedbackForm.query.get_or_404(form_id)
    form_name = feedback_form.form_name
    event_name = feedback_form.event.name
    
    db.session.delete(feedback_form)
    db.session.commit()
    
    flash(f'Feedback form "{form_name}" deleted from event "{event_name}".', 'success')
    return redirect(url_for('feedback_analytics'))


@app.route('/event/<int:event_id>/cancel', methods=['POST'])
@login_required
def cancel_event(event_id):
    """Cancel an event."""
    event = Event.query.get_or_404(event_id)
    if current_user.id != event.creator_id and not current_user.is_admin:
        flash('You do not have permission to cancel this event.', 'danger')
        return redirect(url_for('event_detail', event_id=event.id))
    
    event.status = 'cancelled'
    db.session.commit()
    
    # Notify attendees
    send_event_notification(event, 'event_cancelled')
    
    flash('Event has been cancelled.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/event/<int:event_id>/duplicate', methods=['POST'])
@login_required
def duplicate_event(event_id):
    """Duplicate an event."""
    original_event = Event.query.get_or_404(event_id)
    if current_user.id != original_event.creator_id and not current_user.is_admin:
        flash('You do not have permission to duplicate this event.', 'danger')
        return redirect(url_for('event_detail', event_id=event_id))
    
    # Create new event with same details but new date
    new_event = Event(
        name=f"{original_event.name} (Copy)",
        description=original_event.description,
        start_date=original_event.start_date + timedelta(days=7),  # Default to 1 week later
        end_date=original_event.end_date + timedelta(days=7) if original_event.end_date else None,
        timezone=original_event.timezone,
        location=original_event.location,
        city=original_event.city,
        country=original_event.country,
        capacity=original_event.capacity,
        creator_id=current_user.id,
        visibility=original_event.visibility,
        allow_plus_ones=original_event.allow_plus_ones,
        waitlist_enabled=original_event.waitlist_enabled,
        auto_approval=original_event.auto_approval,
        cover_image_url=original_event.cover_image_url,
        tags=original_event.tags
    )
    
    db.session.add(new_event)
    db.session.commit()
    
    flash('Event duplicated successfully.', 'success')
    return redirect(url_for('event_detail', event_id=new_event.id))


@app.route('/event/<int:event_id>/attendees')
@login_required
def event_attendees(event_id):
    """View and manage event attendees."""
    event = Event.query.get_or_404(event_id)
    if current_user.id != event.creator_id and not current_user.is_admin:
        flash('You do not have permission to view attendees.', 'danger')
        return redirect(url_for('event_detail', event_id=event.id))
    
    attendees = RSVP.query.filter_by(event_id=event.id).order_by(RSVP.created_at.asc()).all()
    
    return render_template('event_attendees.html', event=event, attendees=attendees)


@app.route('/event/<int:event_id>/export')
@login_required
def export_attendees(event_id):
    """Export attendee list to CSV."""
    event = Event.query.get_or_404(event_id)
    if current_user.id != event.creator_id and not current_user.is_admin:
        flash('You do not have permission to export attendees.', 'danger')
        return redirect(url_for('event_detail', event_id=event.id))
    
    attendees = RSVP.query.filter_by(event_id=event.id).all()
    
    # Create CSV content
    csv_content = "Name,Email,Status,Guests,Note,Checked In,RSVP Date\n"
    for rsvp in attendees:
        csv_content += f'"{rsvp.attendee.display_name}","{rsvp.attendee.email}","{rsvp.status}",{rsvp.guests},"{rsvp.note or ""}","{"Yes" if rsvp.checked_in else "No"}","{rsvp.created_at.strftime("%Y-%m-%d %H:%M")}"\n'
    
    from flask import Response
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={event.name}_attendees.csv'}
    )


@app.route('/api/event/<int:event_id>/stats')
@login_required
def event_stats(event_id):
    """API endpoint for event statistics."""
    event = Event.query.get_or_404(event_id)
    if current_user.id != event.creator_id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    stats = {
        'accepted': event.accepted_count,
        'maybe': event.maybe_count,
        'declined': event.declined_count,
        'waitlisted': event.waitlist_count,
        'capacity': event.capacity,
        'available_spots': event.available_spots,
        'checked_in': sum(1 for rsvp in event.rsvps if rsvp.checked_in)
    }
    return jsonify(stats)


@app.route('/event/<int:event_id>/payment', methods=['POST'])
@login_required
def create_payment(event_id):
    """Create a payment for an event."""
    event = Event.query.get_or_404(event_id)
    
    if event.price <= 0:
        flash('This event is free.', 'info')
        return redirect(url_for('event_detail', event_id=event_id))
    
    # Check if user already has an RSVP
    rsvp = RSVP.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    if not rsvp:
        flash('Please RSVP first before making payment.', 'warning')
        return redirect(url_for('event_detail', event_id=event_id))
    
    if rsvp.payment_status == 'paid':
        flash('Payment already completed.', 'info')
        return redirect(url_for('event_detail', event_id=event_id))
    
    # Check if Stripe is available
    if not STRIPE_AVAILABLE:
        flash('Payment system is currently unavailable. Please contact the event organizer.', 'warning')
        return redirect(url_for('event_detail', event_id=event_id))
    
    # Create Stripe checkout session
    success_url = url_for('payment_success', rsvp_id=rsvp.id, _external=True)
    cancel_url = url_for('event_detail', event_id=event_id, _external=True)
    
    session = create_stripe_checkout_session(
        amount=event.price,
        event_name=event.name,
        rsvp_id=rsvp.id,
        success_url=success_url,
        cancel_url=cancel_url,
        currency=app.config.get('DEFAULT_CURRENCY', 'sgd').lower()
    )
    
    if session:
        return redirect(session.url)
    else:
        flash('Failed to create payment session. Please try again.', 'danger')
        return redirect(url_for('event_detail', event_id=event_id))


@app.route('/payment/success/<int:rsvp_id>')
@login_required
def payment_success(rsvp_id):
    """Handle successful payment."""
    rsvp = RSVP.query.get_or_404(rsvp_id)
    
    if rsvp.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('index'))
    
    # Update RSVP status to paid
    rsvp.payment_status = 'paid'
    rsvp.payment_amount = rsvp.event.price
    
    # If capacity allows, set status to Accepted
    if rsvp.event.available_spots > 0:
        rsvp.status = 'Accepted'
    
    db.session.commit()
    
    # Send confirmation email
    send_email(
        to_email=current_user.email,
        subject=f'Payment Confirmation - {rsvp.event.name}',
        body=f'Your payment for {rsvp.event.name} has been confirmed. Amount: ${rsvp.payment_amount:.2f}',
        html_body=f'''
        <h2>Payment Confirmation</h2>
        <p>Your payment for <strong>{rsvp.event.name}</strong> has been confirmed.</p>
        <p><strong>Amount:</strong> ${rsvp.payment_amount:.2f}</p>
        <p><strong>Event Date:</strong> {rsvp.event.start_date.strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Location:</strong> {rsvp.event.location}</p>
        <p>Thank you for your payment!</p>
        '''
    )
    
    flash('Payment successful! You will receive a confirmation email shortly.', 'success')
    return redirect(url_for('event_detail', event_id=rsvp.event_id))


@app.route('/payment/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events."""
    if not STRIPE_AVAILABLE or not app.config.get('STRIPE_WEBHOOK_SECRET'):
        return 'Stripe not available or configured', 400
    
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, app.config['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        rsvp_id = session['metadata']['rsvp_id']
        
        # Update RSVP payment status
        rsvp = RSVP.query.get(rsvp_id)
        if rsvp:
            rsvp.payment_status = 'paid'
            rsvp.payment_amount = session['amount_total'] / 100  # Convert from cents
            rsvp.stripe_payment_intent_id = session['payment_intent']
            db.session.commit()
    
    return 'Success', 200


if __name__ == '__main__':
    # Use port 8080 if FLASK_PORT environment variable is set, otherwise use 5001
    port = int(os.environ.get('FLASK_PORT', 5001))
    app.run(host='0.0.0.0', debug=True, port=port)