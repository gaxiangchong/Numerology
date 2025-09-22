# 🚀 EventApp Quick Start Guide

## 📁 Batch Files Overview

I've created several batch files to make running EventApp super easy:

### 🎯 **Main Files:**
- **`run_eventapp.bat`** - Start the EventApp (use this daily)
- **`setup_eventapp.bat`** - First-time setup (run once)
- **`stop_eventapp.bat`** - Stop the EventApp if needed

---

## 🏃‍♂️ **Quick Start (First Time)**

### **Step 1: First-Time Setup**
1. **Double-click** `setup_eventapp.bat`
2. Follow the prompts to create an admin user
3. Wait for setup to complete

### **Step 2: Run EventApp**
1. **Double-click** `run_eventapp.bat`
2. Wait for the app to start
3. Open your browser to: `http://127.0.0.1:5001`
4. Login with your admin credentials

---

## 📋 **Daily Usage**

### **To Start EventApp:**
- **Double-click** `run_eventapp.bat`
- The app will start automatically
- Open browser to: `http://127.0.0.1:5001`

### **To Stop EventApp:**
- Press `Ctrl+C` in the command window, OR
- **Double-click** `stop_eventapp.bat`

---

## 🔧 **What Each Batch File Does**

### **`run_eventapp.bat`**
- ✅ Activates virtual environment
- ✅ Checks dependencies
- ✅ Starts the Flask server
- ✅ Shows helpful status messages
- ✅ Keeps window open if there are errors

### **`setup_eventapp.bat`**
- ✅ Creates virtual environment (if needed)
- ✅ Installs all required packages
- ✅ Sets up the database
- ✅ Guides you through admin user creation
- ✅ One-time setup for new installations

### **`stop_eventapp.bat`**
- ✅ Stops any running EventApp processes
- ✅ Clean shutdown
- ✅ Useful if the app gets stuck

---

## 🌐 **Accessing the App**

After running `run_eventapp.bat`, you'll see:
```
========================================
  EventApp is starting...
  URL: http://127.0.0.1:5001
  Press Ctrl+C to stop the server
========================================
```

**Open your browser and go to:** `http://127.0.0.1:5001`

---

## 👤 **Admin Accounts**

Your admin accounts are:
- **Username:** `admin` | **Email:** `admin@tester.com`
- **Username:** `admin3` | **Email:** `admin3@tester.com`

Use either of these to login and access admin features.

---

## 🆘 **Troubleshooting**

### **"Virtual environment not found"**
- Run `setup_eventapp.bat` first

### **"Port already in use"**
- Run `stop_eventapp.bat` first
- Then run `run_eventapp.bat` again

### **"Dependencies missing"**
- The batch file will automatically install them
- Or run `setup_eventapp.bat` again

### **App won't start**
- Make sure you're in the correct folder: `D:\GitHub\app.course.rsvp\eventapp`
- Check that `app.py` exists in the folder

---

## 📱 **Features Available**

Once logged in as admin, you can:
- ✅ Create events (single "Create Event" button in top-right)
- ✅ View beautifully designed event cards
- ✅ Manage attendees
- ✅ Export attendee lists
- ✅ View analytics
- ✅ Check-in attendees with QR codes

---

## 🎨 **New Event Card Design**

The event cards now feature:
- 🎯 Professional grid layout
- 🌈 Color-coded status badges
- ✨ Hover effects and animations
- 📱 Mobile-responsive design
- 🎨 Modern typography and spacing

---

**That's it! Just double-click `run_eventapp.bat` to start using EventApp! 🚀**
