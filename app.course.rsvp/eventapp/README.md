# EventApp - Comprehensive Event Management System

A modern, feature-rich event management application built with Flask, designed for seamless deployment on PythonAnywhere.

## 🌟 Features

### Core Functionality
- **User Management**: Registration, authentication, and profile management
- **Event Creation**: Create and manage events with detailed information
- **RSVP System**: Accept/Maybe/Decline responses with guest tracking
- **QR Code Generation**: Unique QR codes for event check-ins
- **Check-in System**: QR code verification and attendee tracking
- **Email Notifications**: Automated email notifications for events and RSVPs

### Advanced Features
- **Analytics Dashboard**: Comprehensive event statistics and reporting
- **Admin Panel**: Full administrative control for organizers
- **Responsive Design**: Modern, mobile-friendly interface
- **Security**: Input validation, password hashing, and secure sessions
- **API Endpoints**: RESTful API for event statistics

### User Roles
- **Attendees**: Can RSVP to events, view their events, manage profile
- **Organizers/Admins**: Can create events, view analytics, manage check-ins

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd eventapp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python app.py
   # Press Ctrl+C to stop
   ```

6. **Create admin user**
   ```bash
   python setup_admin.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open http://localhost:5000 in your browser
   - Register a new account or use the admin account

### PythonAnywhere Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📁 Project Structure

```
eventapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup_admin.py        # Admin user setup script
├── .env.example          # Environment variables template
├── DEPLOYMENT.md         # Deployment guide
├── README.md            # This file
├── templates/           # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── event_detail.html
│   ├── create_event.html
│   ├── update_event.html
│   ├── my_events.html
│   ├── verify.html
│   ├── profile.html
│   └── analytics.html
└── static/              # Static files
    └── qr_codes/        # QR code storage (if needed)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///eventapp.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
APP_NAME=EventApp
ADMIN_EMAIL=admin@yourapp.com
```

### Email Configuration

For Gmail:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in `MAIL_PASSWORD`

## 🎯 Usage Guide

### For Event Organizers

1. **Create an Account**: Register with admin privileges
2. **Create Events**: Use the "Create Event" button to add new events
3. **Manage Events**: Edit event details, view RSVPs, and track attendance
4. **Check-in Attendees**: Use the QR code verification system
5. **View Analytics**: Monitor event performance and attendance statistics

### For Event Attendees

1. **Register**: Create a free account
2. **Browse Events**: View upcoming events on the homepage
3. **RSVP**: Respond to events with Accept/Maybe/Decline
4. **Manage Profile**: Update personal information and notification preferences
5. **Check-in**: Present QR code at event check-in

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Input Validation**: Comprehensive form validation and sanitization
- **Email Validation**: Proper email format verification
- **Session Management**: Secure user sessions with Flask-Login
- **CSRF Protection**: Built-in CSRF protection with Flask-WTF
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Display name
- `email`: Unique email address
- `password_hash`: Hashed password
- `is_admin`: Admin privileges flag
- `email_notifications`: Email preference
- `created_at`: Account creation timestamp

### Events Table
- `id`: Primary key
- `name`: Event name
- `description`: Event description
- `date`: Event date and time
- `location`: Event location
- `capacity`: Maximum attendees
- `creator_id`: Foreign key to Users
- `rsvp_deadline`: RSVP deadline (optional)
- `created_at`: Creation timestamp

### RSVPs Table
- `id`: Primary key
- `event_id`: Foreign key to Events
- `user_id`: Foreign key to Users
- `status`: RSVP status (Accepted/Maybe/Declined)
- `guests`: Number of additional guests
- `qr_code`: Unique QR code for check-in
- `checked_in`: Check-in status
- `created_at`: RSVP timestamp

## 🛠️ API Endpoints

### Public Endpoints
- `GET /`: Homepage with upcoming events
- `GET /login`: Login page
- `POST /login`: User authentication
- `GET /register`: Registration page
- `POST /register`: User registration

### Authenticated Endpoints
- `GET /dashboard`: Organizer dashboard
- `GET /my-events`: User's RSVP'd events
- `GET /profile`: User profile management
- `POST /profile`: Update user profile
- `GET /analytics`: Event analytics (admin only)

### Event Management
- `GET /event/new`: Create event form
- `POST /event/new`: Create new event
- `GET /event/<id>`: Event details and RSVP
- `POST /event/<id>`: Submit RSVP
- `GET /event/<id>/update`: Edit event form
- `POST /event/<id>/update`: Update event

### Check-in System
- `GET /verify`: QR code verification page
- `POST /verify`: Verify and check-in attendee

### API Endpoints
- `GET /api/event/<id>/stats`: Event statistics (JSON)

## 🎨 Customization

### Styling
The application uses Bootstrap 4 for responsive design. You can customize:
- Colors and themes in `base.html`
- Component styling in individual templates
- Add custom CSS in the `static/` directory

### Features
- Add new event fields in the `Event` model
- Extend user profile with additional fields
- Implement new notification types
- Add event categories or tags

## 🐛 Troubleshooting

### Common Issues

1. **Database Errors**
   - Ensure SQLite file has proper permissions
   - Check database path in configuration

2. **Email Not Working**
   - Verify SMTP settings
   - Check app password for Gmail
   - Ensure firewall allows SMTP connections

3. **QR Code Issues**
   - Verify qrcode library installation
   - Check file permissions for QR code storage

4. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path and virtual environment

### Debug Mode
Enable debug mode for development:
```python
app.config['DEBUG'] = True
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For support and questions:
- Check the [Deployment Guide](DEPLOYMENT.md)
- Review the troubleshooting section
- Create an issue in the repository

## 🔮 Future Enhancements

- [ ] Event categories and tags
- [ ] Advanced reporting and exports
- [ ] Mobile app integration
- [ ] Social media integration
- [ ] Payment processing for paid events
- [ ] Multi-language support
- [ ] Advanced user roles and permissions
- [ ] Event templates
- [ ] Automated event reminders
- [ ] Integration with calendar systems

---

**Built with ❤️ using Flask, SQLAlchemy, and Bootstrap**
