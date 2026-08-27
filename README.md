# LAB-01 — local training web app

This is the intentionally vulnerable application defined as **LAB-01** in your
authorized lab dossier (`http://127.0.0.1:8080`, isolated localhost only).
Every vulnerability in it is deliberate and commented in `app.py` with the
STRIDE category and priority it maps to in Section 4.1 of the dossier, so
findings you write up point straight back to that table.

**Run this only inside your isolated lab, per your Rules of Engagement.**
It binds to `127.0.0.1` and must not be exposed to any other network,
container bridge set to `0.0.0.0`, or port-forwarded.

## Setup

```bash
cd lab01-web-app
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:8080`.

Seeded accounts (plaintext, on purpose — see below):

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | admin |
| alice    | alice123  | user  |
| bob      | bob123    | user  |

Reset the database at any time by visiting `/reset-lab`.

## Vulnerabilities included (mapped to your STRIDE table, Section 4.1)

| Route | STRIDE category | Priority | What's wrong |
|---|---|---|---|
| `POST /login` | Tampering | High | Username/password are concatenated directly into a SQL string. Try `admin' -- ` as the username with any password. |
| `GET /profile/<id>` | Tampering | High | IDOR — checks you're logged in, never that you own that profile. Walk `/profile/1`, `/profile/2`, `/profile/3`. |
| `GET /search?q=` | Information disclosure | Medium | Reflected XSS — the query string is rendered with `\|safe`. Try `?q=<script>alert(document.cookie)</script>`. |
| `POST /comments` | Tampering / Information disclosure | High | Stored XSS — comment content is rendered with `\|safe` for every visitor. |
| `GET /admin` | Elevation of privilege | Critical | Checks for *a* session, never `role == admin`. Log in as alice or bob and visit `/admin` directly. |
| App-wide | Information disclosure | Medium | `debug=True` — trigger any unhandled error (e.g. malformed input) to see a full stack trace / interactive debugger. |
| Database | Information disclosure | High | Passwords are stored in plaintext, visible in full on `/admin`. |
| App-wide | Spoofing | High | `app.secret_key` is a static, hardcoded string, so session cookies can be forged offline once the key is known. |

## Suggested exercise flow

1. Enumerate the app manually (Section 4.1's "permitted techniques": low-rate, non-destructive).
2. Confirm each finding above, capture request/response evidence per your Rules of Engagement (Section 5.4).
3. Write each confirmed issue up using the reporting template in Section 6 of your dossier — asset, severity rationale, reproduction steps, impact, evidence, remediation.
4. Cross-check your remediation notes against the "Mitigation" column already in your STRIDE table — they should match what you'd actually recommend fixing here.

## Explicitly out of scope for this app

Per your Rules of Engagement: no denial-of-service or load testing against
it, no attempts to pivot from it to any other host, and no automated
credential-stuffing at scale. This app is for manual, low-rate vulnerability
validation only.
