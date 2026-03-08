# Forgot Password – Email Setup

The app sends password-reset and email-verification links. You can use **SendGrid API**, **SMTP** (Gmail, Resend, Brevo), or other providers.

---

## Option 1: SendGrid API (recommended)

- **Cost**: Free tier **100 emails/day** for 60 days; then paid or other free options  
- **Setup**: API key + verified sender email

1. Sign up at [sendgrid.com](https://sendgrid.com)  
2. Create an API key: Settings → API Keys → Create API Key (Mail Send > Full Access)  
3. Verify a sender: Settings → Sender Authentication → Single Sender Verification (add your email)  
4. Set in `mysite/.env`:

   ```ini
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxx
   MAIL_DEFAULT_SENDER=noreply@yourdomain.com
   ```

5. Install: `pip install sendgrid`  
6. Restart the app. Forgot password and email verification will use SendGrid.

**Note**: `MAIL_DEFAULT_SENDER` must be a verified sender in SendGrid (Single Sender or Domain Authentication).

---

## Option 2: SMTP providers

### Gmail (quick setup)

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

### Resend (SMTP)

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

### Brevo (formerly Sendinblue)

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

### Mailtrap (testing only)

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

If neither **SendGrid API** (`SENDGRID_API_KEY`) nor **SMTP** (`MAIL_SERVER` / `MAIL_USERNAME` / `MAIL_PASSWORD`) is configured:

- The “Forgot password” form still works.  
- After submitting email, the user sees: **“邮件发送失败。请检查服务器邮件配置，或联系管理员。”** (or the English equivalent).  
- No email is sent. You must set one of the options above to actually send reset links.

---

## SendGrid SMTP (alternative to API)

If you prefer SMTP instead of the SendGrid API:

- Server: `smtp.sendgrid.net`
- Port: `587` (TLS)
- Username: `apikey` (literally the string "apikey")
- Password: your SendGrid API key (starts with `SG.`)

```ini
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.xxxxxxxxxxxxxxxx
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

---

## Summary

| Method        | Service   | Free tier        | Best for                    |
|---------------|-----------|------------------|-----------------------------|
| **SendGrid API** | SendGrid  | 100/day (trial)  | Production, reliable         |
| SMTP          | Gmail     | ~500/day         | Small apps, quick setup     |
| SMTP          | Resend    | 3,000/month      | Production                  |
| SMTP          | Brevo     | 300/day          | Production, marketing       |
| SMTP          | Mailtrap  | Unlimited (inbox)| Development/testing only   |

**Recommended**: Use **SendGrid API** (`SENDGRID_API_KEY` + `MAIL_DEFAULT_SENDER`) for production. Fallback to SMTP (Gmail, Resend, Brevo) if preferred.
