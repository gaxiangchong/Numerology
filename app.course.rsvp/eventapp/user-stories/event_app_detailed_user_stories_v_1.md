# Event App – Detailed User Stories (Organizer & Invitee)

This document captures user stories, acceptance criteria, edge cases, and notes for implementation & hosting (PythonAnywhere). Stories are grouped by epics that map to the features visible on the provided screenshot (Home/Dashboard with event cards, organizer badge, attendee counts, Modify, FAB to add, bottom navigation for Home, Past Events, Notifications, My Profile).

---

## Personas & Roles

### Persona: Organizer
- **Profile fields**: first name, last name, display name, email (verified), phone (optional, E.164), profile photo/avatar, timezone, locale, country, city, default event location, notification preferences (email, push/web, SMS), preferred time format (12/24h), account status (active/suspended), privacy settings (show city, show full name).
- **Capabilities**: create/modify/cancel events; set capacity & RSVPs; invite attendees; manage roles; edit event description/time/location; view attendee list & statuses; message attendees; clone events; view analytics (RSVPs over time); manage waitlist; export guest list; manage reminders; transfer ownership.

### Persona: Invitee (Attendee)
- **Profile fields**: first/last name, display name, email (required to RSVP), phone (optional), timezone, locale, dietary/accessibility notes (optional), notification preferences, avatar.
- **Capabilities**: receive invites; view event details; RSVP (Yes/No/Maybe); manage +1 (if allowed); add to calendar; view organizer profile; message organizer; view directions/map; see other attendees (if privacy allows); join waitlist; update RSVP and profile settings.

### System Roles
- **Anonymous Visitor**: can view public events by link but must sign in to RSVP (configurable).
- **Moderator/Admin (optional future)**: can manage reported events/users.

Role-based access control (RBAC) will govern permissions across endpoints and UI actions.

---

## Epic A: Authentication & Onboarding

**A1. Sign Up / Sign In**
- *As a visitor*, I want to create an account using email/password so that I can organize or RSVP to events.
- **Acceptance Criteria**
  - Can sign in/up with email; verification email sent on signup.
  - Password rules: ≥8 chars, 1 upper, 1 lower, 1 number; rate-limited.
  - On first login, user is prompted to set display name, timezone, and avatar.
  - Error states surfaced (wrong password, unverified email).

**A2. Session Management**
- *As a user*, I want my session to persist securely so that I stay logged in across visits.
- **Acceptance**: HttpOnly secure cookies; CSRF tokens for form posts; inactivity timeout (e.g., 30 days remember-me).

**A3. Password Reset**
- *As a user*, I can request a password reset via email.

---

## Epic B: Home/Dashboard – “Your Events”

**B1. View events I organize**
- *As an organizer*, I want to see cards for events I created with key info.
- **Acceptance**
  - Card shows: title, short description, date, start–end time (formatted per profile), city/country (e.g., SG, KL), organizer badge ("Organized"), capacity display `current/limit` (e.g., `1/15`, infinity if none), organizer avatar, action buttons (Modify, Manage Attendees).
  - Cards sorted by next start time (soonest first) by default; sticky grouping by upcoming vs today.
  - Past events suppressed from Home (appear under Past Events).
  - Timezone is user’s profile TZ; hovering or tapping shows event’s local TZ.

**B2. View events I’m invited to**
- *As an invitee*, I want to see my invited events in the same list but with an "Invited" or "Going"/"Maybe" badge.
- **Acceptance**
  - Card badge reflects my RSVP: Invited, Going, Maybe, Not Going.
  - Capacity indicator still visible; if waitlisted, show "Waitlisted".

**B3. Filter/Sort events**
- *As a user*, I can filter by role (Organizing / Invited / All), location, and date range; sort by Start Time or Recently Updated.

**B4. Empty state**
- *As a new organizer*, I see an empty-state CTA to create my first event with the + FAB.

**B5. Load more / pagination**
- *As a user*, additional events load on scroll or via "Load More" (page size configurable).

**B6. Quick actions on card**
- *As an organizer*, I can tap **Modify** to edit the event; I can tap capacity to open the attendee list.
- *As an invitee*, I can RSVP inline from the card (dropdown or buttons) without opening details.

**B7. Accessibility**
- Cards are keyboard navigable; ARIA labels for icons (calendar, clock, location, attendees).

---

## Epic C: Event Creation & Management

**C1. Create an event**
- *As an organizer*, I can create an event from the + Floating Action Button.
- **Fields**: title (required), description (markdown supported), date, start/end time, timezone, location (free text + map optional), capacity (optional), visibility (Public/Private/Unlisted), allow +1s, RSVP options (Yes/No/Maybe), waitlist (on/off), auto-approval, reminders schedule, cover image, tags.
- **Acceptance**
  - Validation on required fields; start < end; timezone defaults to organizer profile.
  - On save, event appears in “Your Events” with the "Organized" badge.

**C2. Edit/Modify an event**
- *As an organizer*, I can edit event details via **Modify** on the card.
- **Acceptance**
  - Changes versioned; attendees notified of significant changes (time/location) with diff summary.
  - Editing capacity adjusts waitlist automatically (promote in FIFO order).

**C3. Cancel or Duplicate event**
- *As an organizer*, I can cancel (with optional message) or duplicate an event.
- **Acceptance**
  - Cancel hides from public listings; attendees receive notification and calendar update.
  - Duplicate clones fields and invites (optional), sets new date/time.

**C4. Manage visibility & sharing**
- *As an organizer*, I can get a shareable link and set if event is discoverable.

**C5. Timezone handling**
- The event stores canonical timezone; invitees see times normalized to their profile timezone with a toggle to view in event’s local timezone.

---

## Epic D: Invitations & RSVPs

**D1. Invite attendees**
- *As an organizer*, I can invite attendees by email upload (CSV) or manual entry; optional personal message.
- **Acceptance**
  - Duplicates and bounces handled; invites sent with deep links; pending invitees listed with status.

**D2. RSVP flow**
- *As an invitee*, I can RSVP from the invite email or event page (Yes/No/Maybe), optionally add a note and +1 details.
- **Acceptance**
  - If capacity reached and waitlist enabled, selecting Yes puts me on waitlist.
  - I can change RSVP up to organizer-defined cutoff.
  - Calendar (.ics) attachment included for Yes/Maybe.

**D3. Guest limit & waitlist**
- *As an organizer*, I can set a capacity and enable waitlist with auto-promotion.
- **Acceptance**
  - Capacity display reflects `confirmed/limit`; waitlisted count shown; promotion sends notification.

**D4. Public RSVP (optional)**
- *As an organizer*, for public events I can allow anyone with the link to RSVP; email verification recommended.

**D5. Communication**
- *As an organizer*, I can message all attendees or a segment (Going/Maybe/Waitlist/No) with updates.

---

## Epic E: Attendee Management

**E1. View attendee list**
- *As an organizer*, I can view attendee statuses and contact info.
- **Acceptance**
  - Columns: Name, Email, RSVP, +1 count, Timestamp, Notes, Check-in (for day of), Actions (promote/demote/waitlist/remove).

**E2. Capacity & counters**
- *As an organizer*, I see real-time counts on the event card (`1/15`), including +1s.

**E3. Export & import**
- *As an organizer*, I can export the attendee list to CSV and import updates.

**E4. Check-in (future)**
- *As an organizer*, I can mark attendees checked-in during the event; QR code optional.

---

## Epic F: Notifications

**F1. In-app notifications (bell in nav)**
- *As a user*, I see a badge count for unread notifications.
- **Events triggering notifications**: new invite, RSVP confirmations/changes, event updates, capacity reached, waitlist promotion, organizer messages, reminders.
- **Delivery**: in-app + email; SMS optional.

**F2. Notification center**
- *As a user*, I can view, mark as read, filter by type, and clear notifications.

**F3. Reminders**
- *As an invitee*, I receive reminders 24h and 1h before start (configurable by organizer).

---

## Epic G: Past Events

**G1. View past events**
- *As a user*, I can see a list of my past events via the bottom nav.
- **Acceptance**
  - Cards similar to Home but labeled "Past"; include links to export attendees or duplicate event.

**G2. Feedback (optional)**
- *As an organizer*, I can request post-event feedback via a simple survey.

---

## Epic H: User Profile (My Profile)

**H1. View & edit profile**
- *As a user*, I can edit profile fields listed in Personas.
- **Acceptance**
  - Avatar upload/crop; timezone picker; language/locale; notification toggles; privacy options (hide surname to invitees, hide attendee list).

**H2. Organizer info on cards**
- *As an invitee*, I can tap the organizer chip/avatar on a card to view their public profile (name, avatar, short bio, verified badge).

**H3. Account deletion**
- *As a user*, I can export my data and delete my account (GDPR-compliant).

---

## Epic I: Navigation & Shell

**I1. Bottom navigation**
- *As a user*, I can navigate between Home, Past Events, Notifications, and My Profile.
- **Acceptance**
  - Active tab highlighted; state preserved when returning from a detail page.

**I2. Floating Action Button (FAB)**
- *As an organizer*, tapping the + opens the Create Event form.
- *As an invitee* without organizer privileges, tapping + prompts to request organizer access or starts a personal event (if allowed).

---

## Epic J: Search & Filters (future)

**J1. Search my events**
- *As a user*, I can search by title, description, location, organizer.

**J2. Location & date filters**
- *As a user*, I can quickly filter to cities (e.g., SG, KL) and date ranges.

---

## Epic K: Security, Privacy, and Compliance

**K1. Privacy controls**
- *As an organizer*, I can set whether attendee list is visible to other attendees.

**K2. Data protection**
- Passwords hashed (Argon2/bcrypt), PII encrypted at rest (where feasible), audit logs for admin actions.

**K3. Rate limiting & abuse**
- Throttle login, invites, and messaging; CAPTCHA on spikes.

**K4. Audit logs (admin)**
- Track critical changes: event edits, capacity changes, cancellations.

---

## Gherkin-style Scenarios (selected)

### Scenario: Card shows correct badges and counts
```
Given I am logged in as Jax (Organizer)
And I have an upcoming event "TTYY" with capacity 15 and 1 confirmed attendee
When I view Home → Your Events
Then I see a card for "TTYY"
And it shows badge "Organized"
And it shows attendee count "1 / 15"
And the Modify action is available
```

### Scenario: Invitee sees RSVP and capacity
```
Given I am invited to "Happy Wedding" with capacity 100
And my RSVP is "Maybe"
When I view Home
Then the card shows badge "Maybe"
And the attendee count reflects confirmed attendees only
And I can change my RSVP inline to Yes or No
```

### Scenario: Waitlist promotion
```
Given an event with capacity 1 is full and waitlist is enabled
And I am #1 on the waitlist
When someone changes their RSVP from Yes to No
Then I am auto-promoted to Confirmed
And I receive an in-app and email notification
```

### Scenario: Timezone display
```
Given the event time is stored in Asia/Singapore 17:30–19:30
And my profile timezone is America/Los_Angeles
When I open the event card
Then the time renders in my local timezone
And I can toggle to view the event’s original timezone
```

### Scenario: Edit capacity promotes waitlist
```
Given 3 people are waitlisted
When the organizer increases capacity by 3
Then all 3 are promoted in FIFO order
And attendees are notified
```

---

## API & Data Model Sketch (for development)

### Core Entities
- **User**: id, email, password_hash, first_name, last_name, display_name, avatar_url, phone, timezone, locale, country, city, preferences (JSON), role, created_at, updated_at, status.
- **Event**: id, owner_id, title, description_md, start_dt (TZ-aware), end_dt (TZ-aware), timezone, location_text, city_code, country_code, visibility, capacity, allow_plus_ones, rsvp_cutoff_dt, cover_url, tags[], created_at, updated_at, status.
- **Invite**: id, event_id, invitee_user_id (nullable until claim), email, token, status (pending/accepted/declined/waitlisted), rsvp (yes/no/maybe), plus_ones, note, timestamps.
- **Notification**: id, user_id, type, payload (JSON), read_at.
- **Checkin (future)**: id, event_id, user_id, checked_in_at.

### Derived counts
- `confirmed_count` (includes +1s if allowed)
- `waitlist_count`

---

## PythonAnywhere Hosting Notes

- **Runtime**: Flask or Django app served via WSGI on PythonAnywhere; use a free tier for dev, paid for custom domain/SSL and higher limits.
- **Database**: MySQL (PythonAnywhere offers managed MySQL) or PostgreSQL via external service; use SQLAlchemy/Django ORM.
- **Static assets**: Collected and served via PythonAnywhere static files config; use a build step if using React front-end (or server-rendered templates with HTMX/Alpine as lightweight option).
- **Background jobs**: Use PythonAnywhere Tasks (scheduled) or a lightweight external worker (e.g., CloudAMQP + worker dyno alternative) for email sends and waitlist promotions; for dev, simulate via cron-like scheduled tasks.
- **Email**: Use an SMTP provider (e.g., SendGrid/Mailgun) for invites, verifications, and notifications.
- **Storage**: PythonAnywhere file storage or external S3-compatible bucket for avatars/cover images.
- **Environment**: keep secrets in PythonAnywhere environment vars; enable HTTPS; set CSRF and session cookie `Secure` and `HttpOnly`.

---

## Non-functional Requirements (NFRs)
- **Performance**: Home loads first 10 upcoming cards in < 800ms P95; pagination or infinite scroll thereafter.
- **Availability**: 99.5% for MVP; graceful degradation when email provider is down.
- **Security**: OWASP Top 10 mitigations; input validation & output escaping; rate limits.
- **Accessibility**: WCAG 2.1 AA for color contrast & focus states.
- **Internationalization**: i18n-ready with translation keys for labels (Organized, Modify, etc.).
- **Observability**: request logging, error reporting (Sentry), basic metrics (RSVP conversion, email bounce).

---

## Definition of Done (per story)
- Unit tests for core logic; integration tests for RSVP and capacity/waitlist; UI tests for card render & actions.
- Security review checklist completed.
- Accessibility checks pass.
- Documentation: API schema and admin runbooks.

---

## Backlog & Next Steps
- Implement Epics in order: A → B → C → D → E → F → G → H → I.
- Seed data and fixtures for SG/KL example.
- Add map integration (OpenStreetMap) and .ics calendar generation.
- Add organizer analytics (basic chart of RSVPs over time).

---

*End of document.*

