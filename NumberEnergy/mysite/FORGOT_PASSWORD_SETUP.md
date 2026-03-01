# Forgot Password – Email Setup

The app sends password-reset links by SMTP. You can use a **free** or paid email service.

---

## Free options (no credit card)

### 1. **Gmail (recommended for small apps)**

- **Cost**: Free  
- **Limit**: ~500 emails/day (Gmail sending limit)  
- **Setup**: Use an **App Password** (not your normal Gmail password).

#### Steps

1. **Turn on 2-Step Verification** (required for App Passwords)  
   - Go to [Google Account → Security](https://myaccount.google.com/security)  
   - Under “How you sign in to Google”, turn on **2-Step Verification**

2. **Create an App Password**  
   - Still in Security → “How you sign in to Google”  
   - Click **App passwords**  
   - Choose “Mail” and “Other (Custom name)”, e.g. “Numerology App”  
   - Copy the **16-character** password (no spaces)

3. **Set environment variables** (before starting the app)

   **Windows (PowerShell, current session):**
   ```powershell
   $env:MAIL_SERVER = "smtp.gmail.com"
   $env:MAIL_PORT = "587"
   $env:MAIL_USE_TLS = "true"
   $env:MAIL_USERNAME = "your.gmail@gmail.com"
   $env:MAIL_PASSWORD = "your-16-char-app-password"
   $env:MAIL_DEFAULT_SENDER = "your.gmail@gmail.com"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set MAIL_SERVER=smtp.gmail.com
   set MAIL_PORT=587
   set MAIL_USE_TLS=true
   set MAIL_USERNAME=your.gmail@gmail.com
   set MAIL_PASSWORD=your-16-char-app-password
   set MAIL_DEFAULT_SENDER=your.gmail@gmail.com
   ```

   **Linux / macOS (bash):**
   ```bash
   export MAIL_SERVER=smtp.gmail.com
   export MAIL_PORT=587
   export MAIL_USE_TLS=true
   export MAIL_USERNAME=your.gmail@gmail.com
   export MAIL_PASSWORD=your-16-char-app-password
   export MAIL_DEFAULT_SENDER=your.gmail@gmail.com
   ```

4. **Optional**: Reset link expiry (default 1 hour)  
   ```powershell
   $env:PASSWORD_RESET_EXPIRY_HOURS = "2"
   ```

5. Start the app (e.g. `python app.py` or `run_local.bat`). Forgot password will send mail via Gmail.

---

### 2. **Resend**

- **Cost**: Free tier **3,000 emails/month**  
- **Setup**: API key, then use SMTP or their API (this app uses SMTP).

1. Sign up at [resend.com](https://resend.com)  
2. Add and verify a domain (or use their free sending domain for testing)  
3. Create an API key  
4. Use Resend’s SMTP:
   - Server: `smtp.resend.com`
   - Port: `465` (SSL) or `587` (TLS)
   - Username: `resend`
   - Password: your **API key**

   **Example (PowerShell):**
   ```powershell
   $env:MAIL_SERVER = "smtp.resend.com"
   $env:MAIL_PORT = "587"
   $env:MAIL_USE_TLS = "true"
   $env:MAIL_USERNAME = "resend"
   $env:MAIL_PASSWORD = "re_xxxxxxxxxxxx"
   $env:MAIL_DEFAULT_SENDER = "onboarding@resend.dev"
   ```

---

### 3. **Brevo (formerly Sendinblue)**

- **Cost**: Free tier **300 emails/day**  
- **Setup**: SMTP with Brevo credentials.

1. Sign up at [brevo.com](https://www.brevo.com)  
2. SMTP: `smtp-relay.brevo.com`, port `587`, TLS  
3. Username: your Brevo login email  
4. Password: create an **SMTP key** in Brevo (Account → SMTP & API)

   **Example (PowerShell):**
   ```powershell
   $env:MAIL_SERVER = "smtp-relay.brevo.com"
   $env:MAIL_PORT = "587"
   $env:MAIL_USE_TLS = "true"
   $env:MAIL_USERNAME = "your@email.com"
   $env:MAIL_PASSWORD = "your-smtp-key"
   $env:MAIL_DEFAULT_SENDER = "your@email.com"
   ```

---

### 4. **Mailtrap (testing only)**

- **Cost**: Free for testing  
- **Use**: Catches all outgoing mail; **does not deliver** to real inboxes. Good for development.

1. Sign up at [mailtrap.io](https://mailtrap.io)  
2. Inbox → SMTP Settings: copy host, port, username, password  
3. Set the same env vars (`MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`, `MAIL_DEFAULT_SENDER`)  
4. Run the app and trigger “Forgot password”; open Mailtrap Inbox to see the reset link.

---

## Making env vars permanent (optional)

**Windows (user env):**  
`Win + R` → `sysdm.cpl` → Advanced → Environment Variables → User variables → New → name `MAIL_SERVER`, value `smtp.gmail.com`, etc.

**`.env` file (if you use python-dotenv):**  
Create `mysite/.env` (and add `.env` to `.gitignore`):

```ini
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your.gmail@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your.gmail@gmail.com
PASSWORD_RESET_EXPIRY_HOURS=1
```

Then in `app.py` you can add at the top (optional):

```python
from dotenv import load_dotenv
load_dotenv()
```

(Install with `pip install python-dotenv`.)

---

## If mail is not configured

If `MAIL_SERVER` / `MAIL_USERNAME` / `MAIL_PASSWORD` are not set:

- The “Forgot password” form still works.  
- After submitting email, the user sees: **“邮件发送失败。请检查服务器邮件配置，或联系管理员。”** (or the English equivalent).  
- No email is sent. You must set one of the options above to actually send reset links.

---

## Summary

| Service   | Free tier        | Best for           |
|----------|------------------|--------------------|
| Gmail    | ~500/day         | Small apps, quick setup |
| Resend   | 3,000/month      | Production, API/SMTP   |
| Brevo    | 300/day          | Production, marketing   |
| Mailtrap | Unlimited (inbox)| Development/testing only |

Use **Gmail + App Password** for a free, simple setup; use **Resend** or **Brevo** when you need more volume or a dedicated sending domain.
