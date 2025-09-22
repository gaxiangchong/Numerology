# 🔐 Admin Account Reset Guide

This guide will help you delete all existing admin accounts and create a fresh admin account.

## ⚠️ **IMPORTANT WARNING**

- **This will delete ALL existing admin accounts permanently**
- **Make sure you have database backup before proceeding**
- **You will lose access to admin functions until you create a new admin**

## 🚀 **Method 1: Using the Interactive Script (Recommended)**

### **Step 1: Run the Interactive Script**

```bash
# Navigate to your project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Run the interactive reset script
python reset_admin_accounts.py
```

### **Step 2: Follow the Prompts**

The script will ask you for:
- New admin username
- New admin email  
- New admin password

### **Step 3: Verify the Reset**

After running the script, you should see:
```
✅ Admin account reset completed successfully!
   - New admin username: [your_username]
   - New admin email: [your_email]
   - Admin privileges: Enabled
   - Email verified: Yes
   - Initial credits: 1000.0
   - Membership: 嫡传 (Diamond)
```

## 🚀 **Method 2: Using the Simple Script (Quick)**

### **Step 1: Run the Simple Script**

```bash
# Navigate to your project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Run the simple reset script
python reset_admin_simple.py
```

### **Step 2: Use Default Credentials**

This creates an admin with:
- **Username:** `admin`
- **Email:** `admin@event.mynoblequest.com`
- **Password:** `admin123`

### **Step 3: Change Password Immediately**

1. Log in with the default credentials
2. Go to your profile page
3. Change the password to something secure

## 🚀 **Method 3: Manual Database Reset (Advanced)**

### **Step 1: Access PythonAnywhere Console**

```bash
# Navigate to your project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Activate virtual environment
source venv/bin/activate

# Start Python shell
python
```

### **Step 2: Run Manual Reset Commands**

```python
# Import required modules
from app import app, db, User
from werkzeug.security import generate_password_hash
from datetime import datetime

# Start app context
with app.app_context():
    # Remove admin privileges from all users
    admin_users = User.query.filter_by(is_admin=True).all()
    for user in admin_users:
        user.is_admin = False
        print(f"Removed admin from: {user.username}")
    
    # Delete all admin users
    for user in admin_users:
        username = user.username
        # Delete associated data
        for rsvp in user.rsvps:
            db.session.delete(rsvp)
        for event in user.created_events:
            for rsvp in event.rsvps:
                db.session.delete(rsvp)
            db.session.delete(event)
        db.session.delete(user)
        print(f"Deleted: {username}")
    
    # Create new admin
    new_admin = User(
        username='admin',
        email='admin@event.mynoblequest.com',
        password_hash=generate_password_hash('admin123'),
        first_name='Admin',
        last_name='User',
        phone='',
        country_code='+65',
        timezone='Asia/Singapore',
        locale='en',
        country='Singapore',
        city='Singapore',
        membership_type='嫡传',
        membership_grade='Diamond',
        credit_point=1000.0,
        is_admin=True,
        email_verified=True,
        account_status='Active',
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_admin)
    db.session.commit()
    print("New admin created successfully!")
```

### **Step 3: Exit Python Shell**

```python
exit()
```

## 🔧 **Troubleshooting**

### **If the script fails:**

1. **Check database connection:**
   ```bash
   python -c "from app import app, db; app.app_context().push(); print('Database connected')"
   ```

2. **Check if users exist:**
   ```bash
   python -c "from app import app, db, User; app.app_context().push(); print([u.username for u in User.query.all()])"
   ```

3. **Manual cleanup:**
   ```bash
   # Delete the database file and recreate
   rm instance/eventapp.db
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### **If you get permission errors:**

```bash
# Make sure you have write permissions
chmod 755 reset_admin_accounts.py
chmod 755 reset_admin_simple.py
```

## ✅ **Verification Steps**

After resetting admin accounts:

1. **Test login with new credentials**
2. **Check admin dashboard access**
3. **Verify admin privileges in member management**
4. **Test event creation functionality**

## 🔒 **Security Recommendations**

1. **Change default password immediately**
2. **Use strong, unique passwords**
3. **Enable email verification**
4. **Regularly backup your database**
5. **Monitor admin account activity**

## 📞 **Need Help?**

If you encounter issues:

1. Check the PythonAnywhere console for error messages
2. Verify database file permissions
3. Ensure virtual environment is activated
4. Check if all dependencies are installed

---

**Remember:** Always backup your database before making major changes!
