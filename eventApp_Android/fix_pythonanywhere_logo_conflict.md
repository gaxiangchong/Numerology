# 🔧 Fix PythonAnywhere Logo Conflict

## Problem
Git merge is failing because there are local changes to the logo file on PythonAnywhere that conflict with your new logo.

## Solution Options

### Option 1: Force Overwrite (Recommended)
This will replace the local logo with your new one:

```bash
# On PythonAnywhere
cd /home/rsvp13/app.course.rsvp/eventapp

# Stash local changes (backup them)
git stash push -m "Backup local logo changes"

# Pull the new logo
git pull origin main

# If you want to see what was stashed:
# git stash list
# git stash show -p stash@{0}
```

### Option 2: Reset and Pull (Clean Slate)
This will completely replace the local version:

```bash
# On PythonAnywhere
cd /home/rsvp13/app.course.rsvp/eventapp

# Reset to match remote
git fetch origin main
git reset --hard origin/main

# This will overwrite all local changes
```

### Option 3: Manual Resolution
If you want to keep some local changes:

```bash
# On PythonAnywhere
cd /home/rsvp13/app.course.rsvp/eventapp

# See what's different
git status
git diff eventapp/static/images/logos/chinese-seal.png

# Choose to keep your version or the remote version
git checkout --theirs eventapp/static/images/logos/chinese-seal.png
# OR
git checkout --ours eventapp/static/images/logos/chinese-seal.png

# Then pull
git pull origin main
```

## Recommended Steps

1. **Use Option 1 (Stash)** - This is the safest approach
2. **After successful pull**, reload your web app in PythonAnywhere dashboard
3. **Test the new logo** at your live site

## Commands to Run

```bash
# On PythonAnywhere
cd /home/rsvp13/app.course.rsvp/eventapp
git stash push -m "Backup local logo changes"
git pull origin main
```

Then reload your web app in PythonAnywhere dashboard.
