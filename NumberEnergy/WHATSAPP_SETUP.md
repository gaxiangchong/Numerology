# WhatsApp configuration guide

This app uses WhatsApp in two ways. Follow the sections that apply to you.

---

## 1. Contact form — “Send via WhatsApp”

When users submit the **Contact** form (service enquiry), they are redirected to WhatsApp with a pre-filled message to your business number.

### What you need

- Your **business WhatsApp number** (the number that should receive these messages).

### Setup steps

1. **Choose where to set the variable**
   - **Option A:** In `NumberEnergy/.env` or `NumberEnergy/mysite/.env` (if your app loads `.env` from there).
   - **Option B:** In your host’s environment (e.g. PythonAnywhere → Web tab → WSGI file / env vars).

2. **Add the variable**
   - Name: `WHATSAPP_BUSINESS_NUMBER`
   - Value: Your full number **without** `+` or spaces.
   - Examples:
     - Malaysia: `60123456789`
     - Singapore: `6591234567`
     - With country code only: `60123456789`

3. **Save and restart**
   - Save the `.env` file or update the host’s env vars, then restart the app so the new value is loaded.

### Format rules

| Correct   | Wrong        |
|----------|--------------|
| `60123456789` | `+60 12-345 6789` |
| `6591234567`  | `+65 9123 4567`   |

The app will strip `+` and spaces, but it’s best to store the number as digits only.

### If you don’t set it

The app uses a placeholder number `60123456789`. The Contact form will still work, but the WhatsApp link will open the wrong number until you set `WHATSAPP_BUSINESS_NUMBER` to your real number.

---

## 2. Login OTP via WhatsApp (Twilio Verify)

Users can log in with a **one-time code sent to their WhatsApp** (no password). This uses **Twilio Verify** with the WhatsApp channel.

### What you need

- A [Twilio](https://www.twilio.com) account.
- Twilio **Verify** service with **WhatsApp** as a channel.

### Step 1: Create a Twilio account

1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio).
2. Sign up (email, password, etc.).
3. Complete phone/email verification if asked.
4. From the [Twilio Console](https://console.twilio.com) you’ll see your **Account SID** and **Auth Token** (click “Show” to reveal the token). You’ll need these later.

### Step 2: Create a Verify service

1. In Twilio Console, open **Explore Products** → **Verify** → **Get started** (or go to [Verify](https://console.twilio.com/us1/develop/verify/services)).
2. Click **Create new** (or **Create Service**).
3. Give it a name (e.g. “My App Login”).
4. Create the service. You’ll get a **Service SID** (starts with `VA...`). Copy and keep it; this is `TWILIO_VERIFY_SERVICE_SID`.

### Step 3: Enable WhatsApp channel

1. Open your Verify service → **Channels** (or **Settings**).
2. Enable **WhatsApp**.
3. Twilio will use their WhatsApp sandbox or your Twilio WhatsApp number. For testing, the sandbox is enough; for production you may need to complete Twilio’s WhatsApp Business approval.
4. Save.

### Step 4: Get your credentials

From the Twilio Console:

| Variable | Where to find it |
|---------|-------------------|
| **Account SID** | Console dashboard (home) — e.g. `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| **Auth Token** | Console dashboard — click “Show” — e.g. `your_auth_token_here` |
| **Verify Service SID** | Verify → Your service → “Service SID” — e.g. `VAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |

### Step 5: Set environment variables

Add these to your `.env` (or your host’s environment):

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_VERIFY_SERVICE_SID=VAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Replace the placeholders with your real values. Restart the app after changing env vars.

### Step 6: Test OTP login

1. Ensure at least one user has a **phone number** (with country code, e.g. `+60123456789`) — set in **Profile** or at **Registration**.
2. On the app, go to **Login** → tab **WhatsApp OTP**.
3. Enter the WhatsApp number (same as in the user’s profile).
4. Click **Send code**. You should receive a 6-digit code on WhatsApp.
5. Enter the code and submit. You should be logged in and optionally prompted to set a password.

### If OTP doesn’t work

- **“WhatsApp login is temporarily unavailable”**  
  One of the three Twilio env vars is missing or wrong. Double-check `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, and `TWILIO_VERIFY_SERVICE_SID` and restart the app.

- **“No account with this WhatsApp number”**  
  No user in your database has that phone number (normalized with country code). Register with that number or add it in Profile.

- **“Could not send code” / “Invalid or expired code”**  
  - Confirm the Verify service has **WhatsApp** enabled.
  - In Twilio, check [Verify → Logs](https://console.twilio.com/us1/develop/verify/logs) for errors.
  - Ensure the phone number is in E.164 format (e.g. `+60123456789`). The app normalizes common inputs (e.g. `012-345 6789` in Malaysia → `+60123456789`).

- **Twilio trial account**  
  Trial accounts can send Verify codes only to **verified** phone numbers. In Twilio Console → Phone Numbers → Manage → Verified Caller IDs, add the test number.

---

## Quick reference

| Purpose | Env variable(s) | Where used |
|--------|------------------|------------|
| Contact form → your business number | `WHATSAPP_BUSINESS_NUMBER` | Contact page “Send via WhatsApp” |
| Login OTP (send/verify code) | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_VERIFY_SERVICE_SID` | Login → WhatsApp OTP tab |

---

## Production notes

- **Contact form:** No API key is used; the form only redirects to `https://wa.me/<number>?text=...`. So you only need the correct `WHATSAPP_BUSINESS_NUMBER` in production.
- **OTP:** For production, use a paid Twilio account and complete [Twilio WhatsApp Business](https://www.twilio.com/docs/whatsapp) setup if you need to send to any number (not just verified test numbers).
- Keep **Auth Token** and **Verify Service SID** secret; do not commit them to version control. Use `.env` (and add `.env` to `.gitignore`) or your host’s secure env configuration.
