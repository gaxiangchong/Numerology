# 🚀 PythonAnywhere Deployment Checklist

## 📋 Pre-Deployment Checklist

### ✅ Code Changes Ready
- [x] Added `membership_type` field to User model
- [x] Created `MEMBERSHIP_TYPES` dictionary with Chinese options
- [x] Added `get_membership_type_info()` helper function
- [x] Updated registration form with phone and membership type fields
- [x] Changed "Type" column header to "YS Type" in member management
- [x] Fixed membership_type update logic in superuser validation
- [x] Added membership_type to template context
- [x] Updated edit modal to include membership_type field
- [x] Database migration completed for membership_type column

### ✅ Files Modified
- `app.py` - Added membership_type field, helper function, and update logic
- `templates/register.html` - Added phone and membership type fields
- `templates/admin_members.html` - Updated to show YS Type column and edit functionality

### ✅ Database Changes
- Added `membership_type` column to user table
- All existing users have `membership_type = 'NA'`
- New users will get membership_type from registration form

---

## 🚀 Deployment Steps

### Step 1: Local Git Operations
```bash
# Navigate to your project directory
cd D:\Github\app.course.rsvp\eventapp

# Check status
git status

# Add all changes
git add .

# Create commit
git commit -m "Deploy: Add membership type system and fix member management

- Add membership_type field to User model with Chinese options
- Update registration form with phone and membership type dropdown  
- Replace Status column with YS Type column in member management
- Fix membership_type update logic in superuser validation
- Add proper separation between membership_grade and membership_type"

# Push to repository
git push origin main
```

### Step 2: PythonAnywhere Deployment
```bash
# SSH into PythonAnywhere
# Navigate to your project directory
cd /home/yourusername/app.course.rsvp/eventapp

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run database migration (if needed)
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Step 3: Reload Web App
1. Go to PythonAnywhere **Web** tab
2. Click **Reload** button
3. Wait for reload to complete

### Step 4: Test New Features
- [ ] Test user registration with phone and membership type
- [ ] Test member management YS Type column display
- [ ] Test editing membership types in admin interface
- [ ] Verify membership_grade and membership_type are separate

---

## 🔧 Configuration Files

### .env File (PythonAnywhere)
Make sure your `.env` file on PythonAnywhere includes:
```env
SECRET_KEY=your-secret-key
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

### WSGI Configuration
Ensure your WSGI file points to the correct path:
```python
import sys
import os

path = '/home/yourusername/app.course.rsvp/eventapp'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

---

## 🧪 Testing Checklist

### Registration Testing
- [ ] New users can register with phone number
- [ ] Membership type dropdown shows: NA, 会员, 家族, 星光, 嫡传
- [ ] Default selection is "NA"
- [ ] Registration completes without email verification

### Member Management Testing
- [ ] YS Type column displays correctly
- [ ] Grade column shows English values (Pending Review, Classic, etc.)
- [ ] YS Type column shows Chinese values (NA, 会员, 家族, etc.)
- [ ] Edit modal includes membership type dropdown
- [ ] Membership type changes save correctly

### Admin Functions Testing
- [ ] Admin can edit user membership types
- [ ] Superuser password validation works
- [ ] Changes are saved to database
- [ ] Page reloads show updated values

---

## 🆘 Troubleshooting

### Common Issues
1. **Import Errors**: Check Python path in WSGI configuration
2. **Database Errors**: Ensure database file has proper permissions
3. **Static Files**: Verify static file mappings in Web tab
4. **Environment Variables**: Check .env file exists and is readable

### Debug Commands
```bash
# Check PythonAnywhere logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# Test Flask app locally on PythonAnywhere
cd /home/yourusername/app.course.rsvp/eventapp
source venv/bin/activate
python app.py
```

---

## 📞 Support

If you encounter issues:
1. Check PythonAnywhere error logs
2. Verify all files were uploaded correctly
3. Ensure virtual environment is activated
4. Check database file permissions
5. Verify environment variables are set

**Ready for Deployment! 🚀**
