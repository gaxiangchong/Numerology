# 🔐 Change Admin Password Guide

This guide will help you change the admin password to `QingHe@81341`.

## 🚀 **Quick Method (Recommended)**

### **Step 1: Run the Simple Script**

```bash
# Navigate to your project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Run the simple password change script
python change_password_simple.py
```

### **Step 2: Verify the Change**

You should see:
```
✅ Admin password updated successfully!
   - Username: admin
   - Email: admin@event.mynoblequest.com
   - New Password: QingHe@81341
```

## 🚀 **Alternative Method: Interactive Script**

### **Step 1: Run the Interactive Script**

```bash
# Navigate to your project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Run the interactive password change script
python change_admin_password.py
```

## 🚀 **Manual Method (Advanced)**

### **Step 1: Access PythonAnywhere Console**

```bash
# Navigate to your project directory
cd /home/rsvp13/app.course.rsvp/eventapp

# Activate virtual environment
source venv/bin/activate

# Start Python shell
python
```

### **Step 2: Run Manual Password Change**

```python
# Import required modules
from app import app, db, User
from werkzeug.security import generate_password_hash

# Start app context
with app.app_context():
    # Find admin user
    admin_user = User.query.filter_by(is_admin=True).first()
    
    if admin_user:
        # Update password
        new_password = "QingHe@81341"
        admin_user.password_hash = generate_password_hash(new_password)
        admin_user.has_default_password = False
        
        db.session.commit()
        print(f"✅ Password changed for {admin_user.username}")
    else:
        print("❌ No admin user found!")
```

### **Step 3: Exit Python Shell**

```python
exit()
```

## ✅ **Verification Steps**

After changing the password:

1. **Test login with new password:**
   - Username: `admin`
   - Password: `QingHe@81341`

2. **Check admin dashboard access**

3. **Verify admin privileges work**

## 🔧 **Troubleshooting**

### **If the script fails:**

1. **Check if admin user exists:**
   ```bash
   python -c "from app import app, db, User; app.app_context().push(); print([u.username for u in User.query.filter_by(is_admin=True).all()])"
   ```

2. **Check database connection:**
   ```bash
   python -c "from app import app, db; app.app_context().push(); print('Database connected')"
   ```

3. **Manual verification:**
   ```bash
   python -c "from app import app, db, User; app.app_context().push(); admin = User.query.filter_by(is_admin=True).first(); print(f'Admin: {admin.username if admin else None}')"
   ```

### **If you get permission errors:**

```bash
# Make sure you have write permissions
chmod 755 change_admin_password.py
chmod 755 change_password_simple.py
```

## 🔒 **Security Notes**

- ✅ Password `QingHe@81341` is strong and secure
- ✅ Password is marked as not default
- ✅ Admin privileges remain intact
- ✅ All existing data is preserved

## 📞 **Need Help?**

If you encounter issues:

1. Check the PythonAnywhere console for error messages
2. Verify database file permissions
3. Ensure virtual environment is activated
4. Check if admin user exists in the database

---

**Remember:** The new password is `QingHe@81341` - make sure to use it exactly as shown!
