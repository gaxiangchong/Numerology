# 🔄 Domain Redirect Setup Guide: rsvp13.pythonanywhere.com → event.mynoblequest.com

## 📋 Overview

This guide helps you set up automatic redirects from your old PythonAnywhere domain `rsvp13.pythonanywhere.com` to your new custom domain `event.mynoblequest.com`.

## 🎯 Why Set Up Redirects?

### **Benefits:**
- ✅ **SEO Preservation** - Maintains search engine rankings
- ✅ **User Experience** - Users with bookmarks still work
- ✅ **Link Preservation** - Old shared links continue to work
- ✅ **Smooth Transition** - No broken links or 404 errors
- ✅ **Professional** - Shows you've properly migrated

## 🛠️ Step-by-Step Setup

### **Step 1: Create Redirect Web App on PythonAnywhere**

1. **Go to PythonAnywhere Dashboard**
   - Login to [pythonanywhere.com](https://pythonanywhere.com)
   - Click on "Web" tab

2. **Add New Web App for Redirect**
   - Click "Add a new web app"
   - Select "Manual configuration"
   - Choose Python 3.10
   - **Domain**: `rsvp13.pythonanywhere.com`

### **Step 2: Configure the Redirect Web App**

1. **Set Source Code**
   - **Source code**: `/home/rsvp13/app.course.rsvp`
   - **Working directory**: `/home/rsvp13/app.course.rsvp`

2. **Set WSGI File**
   - **WSGI file**: `/home/rsvp13/app.course.rsvp/wsgi_redirect.py`

### **Step 3: Upload Redirect Files**

1. **On PythonAnywhere Console**
   ```bash
   # Navigate to your project directory
   cd /home/rsvp13/app.course.rsvp
   
   # Pull latest changes (if not already done)
   git pull origin main
   
   # Verify redirect files are present
   ls -la redirect_old_domain.py
   ls -la wsgi_redirect.py
   ```

2. **Set Proper Permissions**
   ```bash
   # Make WSGI file executable
   chmod 644 wsgi_redirect.py
   
   # Make redirect script executable
   chmod 644 redirect_old_domain.py
   ```

### **Step 4: Test the Redirect**

1. **Reload the Web App**
   - Go to PythonAnywhere Web tab
   - Click "Reload" button for the redirect web app

2. **Test the Redirect**
   - Visit `http://rsvp13.pythonanywhere.com`
   - Should redirect to `https://event.mynoblequest.com`
   - Test with different paths: `http://rsvp13.pythonanywhere.com/login`
   - Should redirect to `https://event.mynoblequest.com/login`

## 🔧 Redirect Configuration Details

### **Redirect Types Implemented:**

#### **1. Home Page Redirect**
```python
@app.route('/')
def redirect_home():
    return redirect('https://event.mynoblequest.com/', code=301)
```

#### **2. All Paths Redirect**
```python
@app.route('/<path:path>')
def redirect_all(path):
    return redirect(f'https://event.mynoblequest.com/{path}', code=301)
```

#### **3. Static Files Redirect**
```python
@app.route('/static/<path:filename>')
def redirect_static(filename):
    return redirect(f'https://event.mynoblequest.com/static/{filename}', code=301)
```

### **HTTP Status Codes Used:**

- **301 (Moved Permanently)** - Tells search engines the redirect is permanent
- **SEO-friendly** - Preserves search rankings
- **Browser-friendly** - Browsers cache the redirect

## 📱 Testing Your Redirects

### **Test Checklist:**

#### **Basic Redirects:**
- [ ] `http://rsvp13.pythonanywhere.com` → `https://event.mynoblequest.com`
- [ ] `http://rsvp13.pythonanywhere.com/` → `https://event.mynoblequest.com/`
- [ ] `http://rsvp13.pythonanywhere.com/login` → `https://event.mynoblequest.com/login`
- [ ] `http://rsvp13.pythonanywhere.com/register` → `https://event.mynoblequest.com/register`

#### **Static Files:**
- [ ] `http://rsvp13.pythonanywhere.com/static/css/style.css` → `https://event.mynoblequest.com/static/css/style.css`
- [ ] `http://rsvp13.pythonanywhere.com/static/images/logo.png` → `https://event.mynoblequest.com/static/images/logo.png`

#### **Event Pages:**
- [ ] `http://rsvp13.pythonanywhere.com/events/123` → `https://event.mynoblequest.com/events/123`
- [ ] `http://rsvp13.pythonanywhere.com/my-events` → `https://event.mynoblequest.com/my-events`

### **Testing Commands:**

```bash
# Test redirect with curl
curl -I http://rsvp13.pythonanywhere.com

# Should return:
# HTTP/1.1 301 Moved Permanently
# Location: https://event.mynoblequest.com/
```

## 🚨 Troubleshooting

### **Common Issues:**

#### **1. Redirect Not Working**
```bash
# Check if redirect web app is running
# Go to PythonAnywhere Web tab
# Check "Error log" for any issues
```

**Solution:**
- Verify WSGI file path is correct
- Check file permissions
- Ensure redirect script is accessible

#### **2. Infinite Redirect Loop**
**Symptoms:** Browser shows "too many redirects" error

**Solution:**
- Check that redirect target is different from source
- Verify HTTPS is properly configured
- Test with different browser/incognito mode

#### **3. 404 Errors**
**Symptoms:** Old URLs return 404 instead of redirecting

**Solution:**
- Verify redirect web app is active
- Check PythonAnywhere error logs
- Test redirect script locally first

#### **4. SSL Certificate Issues**
**Symptoms:** HTTPS redirects fail

**Solution:**
- Ensure SSL is enabled for both domains
- Check PythonAnywhere SSL status
- Wait for certificate propagation

### **Debug Commands:**

```bash
# Check redirect web app status
ps aux | grep python

# Check error logs
tail -f /var/log/rsvp13.pythonanywhere.com.error.log

# Test redirect script locally
python redirect_old_domain.py
```

## 📊 Monitoring Redirects

### **Analytics Setup:**

1. **Google Analytics**
   - Add tracking to redirect script
   - Monitor traffic from old domain
   - Track redirect success rates

2. **Server Logs**
   - Monitor redirect requests
   - Check for 404 errors
   - Track redirect performance

### **Performance Monitoring:**

```bash
# Monitor redirect performance
# Check response times
# Monitor server load
```

## 🔄 Advanced Redirect Options

### **Custom Redirect Messages:**

You can customize the redirect to show a message:

```python
from flask import Flask, redirect, render_template_string

@app.route('/')
def redirect_with_message():
    return render_template_string('''
    <html>
    <head>
        <meta http-equiv="refresh" content="3;url=https://event.mynoblequest.com/">
        <title>Redirecting...</title>
    </head>
    <body>
        <h1>We've moved!</h1>
        <p>Redirecting to our new domain...</p>
        <p><a href="https://event.mynoblequest.com/">Click here if not redirected automatically</a></p>
    </body>
    </html>
    ''')
```

### **Selective Redirects:**

```python
# Redirect only specific paths
@app.route('/old-page')
def redirect_old_page():
    return redirect('https://event.mynoblequest.com/new-page', code=301)

# Keep some paths on old domain
@app.route('/legacy')
def keep_legacy():
    return "This page stays on the old domain"
```

## 📈 SEO Considerations

### **Search Engine Optimization:**

1. **301 Redirects** - Preserve search rankings
2. **Canonical URLs** - Point to new domain
3. **Sitemap Updates** - Update sitemap with new URLs
4. **Google Search Console** - Submit domain change

### **SEO Checklist:**

- [ ] All old URLs redirect to new domain
- [ ] 301 status codes are used
- [ ] No broken links remain
- [ ] Sitemap updated with new URLs
- [ ] Google Search Console notified

## 🎉 Success!

Once set up, your redirects will:

- ✅ **Automatically redirect** all old URLs to new domain
- ✅ **Preserve SEO rankings** with 301 redirects
- ✅ **Maintain user experience** with seamless transitions
- ✅ **Handle all paths** including static files and dynamic routes
- ✅ **Provide professional migration** without broken links

### **Final Testing:**

1. **Test all major URLs** from old domain
2. **Verify redirects work** in different browsers
3. **Check mobile redirects** on mobile devices
4. **Monitor for any issues** in the first few days

Your users will now be automatically redirected from the old domain to your new domain! 🚀✨
