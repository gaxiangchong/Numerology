# Deploy to Production (PythonAnywhere)

This guide walks you through updating your production app at **bazipro.pythonanywhere.com**, including code changes and database migrations.

---

## Prerequisites

- PythonAnywhere account (username: **bazipro**)
- SSH or Bash console access on PythonAnywhere
- Your project path: `/home/bazipro/numerology-app`

---

## Step 1: Push Your Code to Git (if using Git)

On your local machine:

```bash
cd D:\GitHub\Numerology
git add .
git status
git commit -m "Update: forgot password, sendgrid, migrations"
git push origin main
```

---

## Step 2: Connect to PythonAnywhere

1. Go to [https://www.pythonanywhere.com](https://www.pythonanywhere.com) and log in
2. Open the **Consoles** tab
3. Start a **Bash** console

---

## Step 3: Pull Latest Code

In the Bash console:

```bash
cd /home/bazipro/numerology-app
git pull origin main
```

If you don't use Git, upload your updated files via the **Files** tab instead.

---

## Step 4: Update Dependencies

Install any new packages (e.g. `sendgrid`):

```bash
cd /home/bazipro/numerology-app
pip install -r requirements.txt --user
```

Or install sendgrid explicitly:

```bash
pip install sendgrid --user
```

---

## Step 5: Run Database Migrations

**Option A: Flask-Migrate (recommended)**

```bash
cd /home/bazipro/numerology-app
export FLASK_APP=mysite/app.py
flask db upgrade
```

**Option B: If Flask-Migrate fails or you use migrate_db.py**

```bash
cd /home/bazipro/numerology-app/mysite
python migrate_db.py
```

**Option C: Manual Alembic (if flask db doesn't work)**

```bash
cd /home/bazipro/numerology-app/mysite
alembic upgrade head
```

---

## Step 6: Set Environment Variables

1. Go to **Web** tab → your app
2. Click **Edit** next to "Code" or find **Environment variables**
3. Add/update these (especially for forgot password):

| Variable | Example | Notes |
|----------|---------|-------|
| `SECRET_KEY` | (your secret) | Required |
| `SENDGRID_API_KEY` | SG.xxx... | For forgot password emails |
| `MAIL_DEFAULT_SENDER` | app.yishu@outlook.com | Verified sender in SendGrid |
| `DATABASE_URL` | sqlite:///users.db | Or your DB path |
| `YOUR_DOMAIN` | https://bazipro.pythonanywhere.com | For links in emails |

---

## Step 7: Reload the Web App

1. Go to **Web** tab
2. Click the green **Reload** button for your app

---

## Quick Checklist

- [ ] Code pulled/uploaded
- [ ] `pip install -r requirements.txt --user` (or `pip install sendgrid --user`)
- [ ] `flask db upgrade` or `python migrate_db.py` (in mysite)
- [ ] Environment variables set (SENDGRID_API_KEY, MAIL_DEFAULT_SENDER)
- [ ] Web app reloaded

---

## Troubleshooting

### Internal Server Error (e.g. on login)

**1. Check the error log (most important)**

On PythonAnywhere:
1. Go to **Web** tab
2. Scroll to **Log files**
3. Click **Error log** — this shows the full Python traceback

Common causes:
- **"no such column"** → Database schema is out of date. Run migrations (Step 5 above).
- **"no such table"** → Same: run `flask db upgrade` or `python migrate_db.py`.
- **Database path wrong** → Set `DATABASE_URL` in Web → Environment variables, e.g.:
  `sqlite:////home/bazipro/numerology-app/mysite/instance/users.db` (4 slashes for absolute path)

**2. Run migrations if you haven't**

```bash
cd /home/bazipro/numerology-app
export FLASK_APP=mysite/app.py
flask db upgrade
```

Or:

```bash
cd /home/bazipro/numerology-app/mysite
python migrate_db.py
```

**3. Ensure DATABASE_URL is correct**

In **Web** → **Environment variables**, add:
```
DATABASE_URL=sqlite:////home/bazipro/numerology-app/mysite/instance/users.db
```
(Use 4 slashes for an absolute path. Create `mysite/instance` if it doesn't exist: `mkdir -p mysite/instance`)

**4. "no such column: user.day_master"**

The app expects `day_master` but your DB doesn't have it. Run:

```bash
cd /home/bazipro/numerology-app/mysite
# If your Web app uses DATABASE_URL from Web tab, set it here too:
export DATABASE_URL="sqlite:////home/bazipro/numerology-app/mysite/instance/users.db"
python add_day_master_column.py
```

Or add the column directly (find your DB path first):
```bash
find /home/bazipro -name "users.db" 2>/dev/null
sqlite3 /path/to/users.db "ALTER TABLE user ADD COLUMN day_master VARCHAR(10);"
```

### "SendGrid library not installed"
Run: `pip install sendgrid --user` in the Bash console, then reload the app.

### Migration errors
- Check `mysite/migrations/versions/` for the migration chain
- If `flask db upgrade` fails, try `python migrate_db.py` (handles common schema changes)
- Backup your DB first: `cp mysite/instance/users.db mysite/instance/users.db.bak`

### WSGI path
Your `wsgi.py` should point to `/home/bazipro/numerology-app`. Verify in **Web** → **WSGI configuration file**.
