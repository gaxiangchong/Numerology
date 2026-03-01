# Quick Update Guide (Already Deployed App)

Use this when the app is **already deployed** (e.g. on PythonAnywhere) and you need to **update code or config** without a full first-time setup.

---

## 1. Get the latest code

- **Git:** In your project directory on the server:
  ```bash
  cd /home/yourusername/numerology-app   # or your app path
  git pull
  ```
- Or re-upload the changed files (e.g. via Git, SFTP, or PythonAnywhere Files).

---

## 2. Environment variables (required for login and stability)

Set these in your hosting environment (e.g. PythonAnywhere **Web** → your app → **Environment variables** or a `.env` file in the project):

| Variable | Purpose |
|----------|--------|
| **SECRET_KEY** | **Required for login.** If missing or wrong, login can return a server error. Use a long random string (e.g. `openssl rand -hex 32`). |
| **DATABASE_URL** or **SQLALCHEMY_DATABASE_URI** | SQLite path in production should be **absolute**, e.g. `sqlite:////home/yourusername/numerology-app/mysite/instance/users.db` so the DB is found after restart. |

Optional but recommended:

- **YOUR_DOMAIN** – Your site URL (e.g. `https://yourusername.pythonanywhere.com`) for Stripe and links.
- **STRIPE_SECRET_KEY**, **STRIPE_WEBHOOK_SECRET** – If you use Stripe.
- **MAIL_*** ** – If you use “forgot password” email.

---

## 3. Install dependencies and run migrations

In a **Bash console** on the server (or SSH), from the **project root** (parent of `mysite`):

```bash
cd /home/yourusername/numerology-app
source venv/bin/activate   # or: source mysite/venv/bin/activate if venv is inside mysite
pip install -r requirements.txt
export FLASK_APP=mysite/app.py
flask db upgrade
```

- If you use a virtualenv in a different path, activate that one.
- If `flask db upgrade` fails, check that **DATABASE_URL** / **SQLALCHEMY_DATABASE_URI** points to the same DB file the app uses.

---

## 4. Restart the web app

- **PythonAnywhere:** **Web** tab → your app → **Reload**.
- Other hosts: restart the process that runs the WSGI app (e.g. gunicorn, uWSGI, or the platform’s “Restart” button).

---

## 5. If login still returns “server error”

1. **Set SECRET_KEY**  
   The app uses it for session signing. If it’s missing or changed, login can 500. Set a new value in the environment and restart.

2. **Use an absolute database path**  
   Set **DATABASE_URL** (or **SQLALCHEMY_DATABASE_URI**) to an absolute SQLite path, e.g.  
   `sqlite:////home/yourusername/numerology-app/mysite/instance/users.db`  
   Create the `instance` folder if needed:  
   `mkdir -p mysite/instance`

3. **Run migrations**  
   Ensure the DB schema is up to date:  
   `FLASK_APP=mysite/app.py flask db upgrade`

4. **Check error logs**  
   On PythonAnywhere: **Web** → **Error log**. Look for `KeyError`, `OperationalError`, or stack traces to see if the failure is session, database, or missing env.

---

## Checklist

- [ ] Code updated (git pull or upload).
- [ ] **SECRET_KEY** set in environment (and reloaded).
- [ ] **DATABASE_URL** or **SQLALCHEMY_DATABASE_URI** set to absolute path.
- [ ] `pip install -r requirements.txt` and `flask db upgrade` run.
- [ ] Web app restarted.

After that, try logging in again. If it still fails, the server error log will point to the exact cause.
