# Deployment Guide for Feature v0.2

## 🚀 Safe Deployment to PythonAnywhere

This guide ensures that the new features are deployed without affecting the existing production database.

## 📋 Pre-Deployment Checklist

### 1. Database Compatibility
- ✅ All new features are backward compatible
- ✅ New database columns have default values
- ✅ Existing data will not be affected
- ✅ Migration scripts are included for new fields

### 2. New Features in v0.2
- ⭐ **Star Rating System**: Beautiful gold star ratings for feedback forms
- 📊 **Member Export**: CSV export functionality for all member data
- 🌐 **Language Support**: English/Chinese language switching
- 💬 **Enhanced Feedback**: Improved feedback system on My Events page
- 🔐 **Password Reset**: Admin password reset with immediate login
- 📧 **Email Verification**: Re-enabled with proper migration support

## 🔧 Deployment Steps

### Step 1: Pull the New Branch
```bash
# In PythonAnywhere Bash Console
cd /home/rsvp13/app.course.rsvp/eventapp
git fetch origin
git checkout feature/v0.2
git pull origin feature/v0.2
```

### Step 2: Database Migrations (Safe - Won't Affect Existing Data)
```bash
# Run these commands in PythonAnywhere Python Console
# These are safe migrations that only add new columns with default values

# 1. Add feedback_enabled column to Event table
python -c "
import sqlite3
conn = sqlite3.connect('instance/eventapp.db')
cursor = conn.cursor()
try:
    cursor.execute('ALTER TABLE event ADD COLUMN feedback_enabled BOOLEAN DEFAULT 0')
    cursor.execute('UPDATE event SET feedback_enabled = 0 WHERE feedback_enabled IS NULL')
    conn.commit()
    print('✅ feedback_enabled column added successfully')
except sqlite3.Error as e:
    if 'duplicate column name' in str(e):
        print('✅ feedback_enabled column already exists')
    else:
        print(f'❌ Error: {e}')
finally:
    conn.close()
"

# 2. Add has_default_password column to User table
python -c "
import sqlite3
conn = sqlite3.connect('instance/eventapp.db')
cursor = conn.cursor()
try:
    cursor.execute('ALTER TABLE user ADD COLUMN has_default_password BOOLEAN DEFAULT 0')
    cursor.execute('UPDATE user SET has_default_password = 0 WHERE has_default_password IS NULL')
    conn.commit()
    print('✅ has_default_password column added successfully')
except sqlite3.Error as e:
    if 'duplicate column name' in str(e):
        print('✅ has_default_password column already exists')
    else:
        print(f'❌ Error: {e}')
finally:
    conn.close()
"
```

### Step 3: Restart the Web Application
```bash
# In PythonAnywhere Web tab
# Click "Reload" button to restart the application
```

### Step 4: Verify Deployment
1. **Check Application Status**: Ensure the app loads without errors
2. **Test New Features**:
   - Language switch button (top right)
   - Star ratings in feedback forms
   - Member export button in admin panel
   - Enhanced feedback system on My Events page

## 🛡️ Safety Measures

### Database Safety
- **No Data Loss**: All migrations only add new columns with default values
- **Backward Compatibility**: Existing functionality remains unchanged
- **Rollback Ready**: Can easily switch back to main branch if needed

### Feature Safety
- **Admin Only**: Export feature is restricted to administrators
- **Optional Features**: New features are enhancements, not requirements
- **Graceful Degradation**: App works even if new features fail

## 🔄 Rollback Plan (If Needed)

If any issues occur, you can easily rollback:

```bash
# In PythonAnywhere Bash Console
cd /home/rsvp13/app.course.rsvp/eventapp
git checkout main
git pull origin main

# Then restart the web application
```

## 📊 New Features Overview

### 1. Star Rating System
- **Location**: Feedback forms
- **Benefit**: More intuitive and attractive rating interface
- **Impact**: Better user experience

### 2. Member Export
- **Location**: Admin Members page
- **Access**: Admin only
- **Benefit**: Easy data export for analysis and reporting

### 3. Language Support
- **Location**: Top right corner of all pages
- **Languages**: English/Chinese
- **Benefit**: Better accessibility for Chinese users

### 4. Enhanced Feedback
- **Location**: My Events page
- **Benefit**: More accessible feedback system
- **Logic**: Shows for any RSVP when admin enables feedback

### 5. Password Reset Flow
- **Location**: Admin member management
- **Benefit**: Admins can reset user passwords with immediate access
- **Security**: Requires superuser password confirmation

## ✅ Post-Deployment Verification

After deployment, verify these features work:

1. **Language Switch**: Click language button, verify text changes
2. **Star Ratings**: Go to feedback form, verify gold stars appear
3. **Member Export**: As admin, click export button, verify CSV downloads
4. **Feedback System**: Enable feedback for an event, verify buttons appear
5. **Password Reset**: As admin, reset a user password, verify immediate login

## 📞 Support

If you encounter any issues:
1. Check the PythonAnywhere error logs
2. Verify database migrations completed successfully
3. Ensure all files were pulled correctly
4. Restart the web application if needed

## 🎉 Success!

Once deployed successfully, you'll have:
- Beautiful star rating system
- Comprehensive member export functionality
- Bilingual language support
- Enhanced feedback system
- Improved admin password management

All while maintaining full compatibility with your existing production data!
