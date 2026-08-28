# Remediation Guide

## Overview

This document provides specific, actionable remediation guidance for each deliberate vulnerability in LAB-01. The vulnerable application in `app.py` is **intentionally left unchanged** — it exists for training validation. Secure implementations are demonstrated in `secure-examples/` for educational comparison.

**Principle**: Fix the root cause, not the symptom. Each remediation addresses the specific code/configuration flaw.

---

## T-001: SQL Injection in Login (`POST /login`)

### Current Weakness
```python
# app.py:106-112
query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(
    username, password
)
row = db.execute(query).fetchone()
```
User input directly concatenated into SQL string. Payload `admin' -- ` comments out password check.

### Why Dangerous
- Authentication bypass as any user (including admin)
- Potential UNION-based data exfiltration of entire database
- No authentication required (pre-auth vulnerability)
- Enables full account takeover

### Secure Implementation
**Parameterized Queries** (primary fix):
```python
# Secure version
query = "SELECT * FROM users WHERE username = ? AND password = ?"
row = db.execute(query, (username, password)).fetchone()
```

**Defense in Depth**:
```python
# Input validation (allowlist)
import re
if not re.match(r'^[a-zA-Z0-9_]{3,32}$', username):
    return "Invalid username format", 400

# Password hashing (see T-007)
# row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
# if row and check_password_hash(row['password'], password):
#     # login success
```

### Expected Security Improvement
- SQL injection eliminated in login endpoint
- Input treated as data, never as code
- Foundation for securing all database interactions

### Retest Objective
1. Submit `admin' -- ` as username with any password
2. Verify login fails with "Invalid username or password"
3. Verify legitimate login (admin/admin123) still works
4. Verify no database errors or anomalous behavior

---

## T-002: IDOR in Profile Access (`GET /profile/<id>`)

### Current Weakness
```python
# app.py:136-148
@app.route("/profile/<int:user_id>")
def profile(user_id):
    if "user_id" not in session:  # Only checks authentication
        return redirect(url_for("login"))
    target = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    # No ownership check!
    notes = db.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,)).fetchall()
    return render_template("profile.html", target=target, notes=notes, viewer=session)
```

### Why Dangerous
- Any authenticated user accesses any other user's profile
- Exposes PII (emails) and sensitive notes (VPN keys, test card data)
- Horizontal privilege escalation
- Parameterized query used correctly — but authorization missing

### Secure Implementation
**Ownership Check** (primary fix):
```python
@app.route("/profile/<int:user_id>")
def profile(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Authorization: users can only view their own profile
    if session["user_id"] != user_id and session.get("role") != "admin":
        return "Forbidden: You can only view your own profile.", 403
    
    target = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if target is None:
        return "No such user.", 404
    notes = db.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,)).fetchall()
    return render_template("profile.html", target=target, notes=notes, viewer=session)
```

**Alternative: Resource-Based Access Control (ReBAC)**
```python
def can_view_profile(viewer_id, viewer_role, target_id):
    return viewer_id == target_id or viewer_role == "admin"

@app.route("/profile/<int:user_id>")
def profile(user_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if not can_view_profile(session["user_id"], session.get("role"), user_id):
        return "Forbidden", 403
    # ...
```

### Expected Security Improvement
- Users confined to their own data
- Admin retains cross-user access (legitimate)
- Horizontal privilege escalation eliminated

### Retest Objective
1. Login as alice (user_id=2)
2. Visit `/profile/1` (admin) → Expect 403 Forbidden
2. Visit `/profile/3` (bob) → Expect 403 Forbidden
3. Visit `/profile/2` (own) → Expect success
4. Login as admin → Visit all profiles → Expect success

---

## T-003: Reflected XSS in Search (`GET /search?q=`)

### Current Weakness
```html
<!-- templates/search.html:9 -->
<p>Search results for: {{ query|safe }}</p>
```
The `|safe` filter disables Jinja2 auto-escaping, rendering raw HTML/JS.

### Why Dangerous
- Attacker crafts malicious link with script payload
- Victim clicks link → script executes in victim's browser
- Session cookie theft, credential harvesting, defacement
- No CSP header to mitigate

### Secure Implementation
**Remove `|safe` Filter** (primary fix):
```html
<!-- Secure version -->
<p>Search results for: {{ query }}</p>
```
Jinja2 auto-escaping is enabled by default — `|safe` explicitly disables it.

**Content Security Policy** (defense in depth):
```python
# app.py - add after app creation
@app.after_request
def add_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response
```

**Input Validation** (additional):
```python
@app.route("/search")
def search():
    q = request.args.get("q", "")
    # Limit length, allow safe chars only
    if len(q) > 100:
        q = q[:100]
    return render_template("search.html", query=q)
```

### Expected Security Improvement
- User input auto-escaped in HTML context
- Script tags rendered as text: `<script>alert(1)</script>`
- CSP provides second layer against injection

### Retest Objective
1. Visit `/search?q=<script>alert('XSS')</script>`
2. Observe: script rendered as text, no alert dialog
3. Verify legitimate search queries display correctly
4. Verify CSP header present in response

---

## T-004: Stored XSS in Comments (`POST /comments`)

### Current Weakness
```html
<!-- templates/comments.html:11 -->
<p><strong>{{ c['author'] }}:</strong> {{ c['content']|safe }}</p>
```
Stored comment content rendered with `|safe` for every visitor.

### Why Dangerous
- **Persistent**: Payload stored in database, executes for ALL visitors
- **Wide impact**: Affects admin, other users, future visitors
- **Stealth**: No suspicious link needed — just visit `/comments`
- **Chaining**: Can steal admin session → full system compromise

### Secure Implementation
**Remove `|safe` Filter** (primary fix):
```html
<!-- Secure version -->
<p><strong>{{ c['author'] }}:</strong> {{ c['content'] }}</p>
```

**Allowlist Sanitization** (if rich text needed):
```python
# secure-examples/sanitize.py
import bleach

ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
ALLOWED_ATTRS = {}

def sanitize_html(content):
    return bleach.clean(content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)

# In comments route:
# content = sanitize_html(request.form.get("content", ""))
```

**CSP Header** (same as T-003 — defense in depth)

### Expected Security Improvement
- Stored payloads rendered as harmless text
- No script execution for any visitor
- Legitimate text formatting preserved (if sanitizer used)

### Retest Objective
1. Post comment: `<script>alert('Stored')</script>`
2. Visit `/comments` in same session → Observe: text rendered, no alert
3. Visit `/comments` in incognito/new browser → Observe: text rendered, no alert
4. Verify legitimate comments (plain text) display correctly

---

## T-005: Broken Authorization in Admin Panel (`GET /admin`)

### Current Weakness
```python
# app.py:178-187
@app.route("/admin")
def admin():
    if "user_id" not in session:  # Only checks authentication
        return redirect(url_for("login"))
    # NO ROLE CHECK!
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("admin.html", users=users)
```

### Why Dangerous
- **Vertical privilege escalation**: Any user → admin panel
- **Information disclosure**: All plaintext passwords exposed
- **Critical severity**: Enables full system compromise
- **Simple fix missing**: Single `if session.get('role') != 'admin'` check

### Secure Implementation
**Role-Based Access Control** (primary fix):
```python
# Decorator approach (reusable)
from functools import wraps

def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if session.get("role") != required_role:
                return "Forbidden: Insufficient privileges.", 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Usage:
@app.route("/admin")
@require_role("admin")
def admin():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("admin.html", users=users)
```

**Inline Check** (simpler):
```python
@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return "Forbidden: Admin access required.", 403
    # ...
```

### Expected Security Improvement
- Non-admin users receive 403 Forbidden
- Admin panel accessible only to role=admin
- Plaintext passwords no longer exposed to regular users

### Retest Objective
1. Login as alice (role=user)
2. Visit `/admin` → Expect 403 Forbidden
2. Login as admin (role=admin)
3. Visit `/admin` → Expect success, user table displayed
4. Verify passwords still visible to admin (separate issue: T-007)

---

## T-006: Debug Mode Information Disclosure

### Current Weakness
```python
# app.py:25
app.debug = True
```
Enables Werkzeug debugger with stack traces, source code, interactive console.

### Why Dangerous
- Unhandled errors leak full stack traces + source code
- Interactive debugger enables RCE if PIN known
- Internal architecture, file paths, variable state exposed
- Violates production security basics

### Secure Implementation
**Disable Debug Mode** (primary fix):
```python
# app.py:25
app.debug = False  # Or remove line — defaults to False
```

**Production Error Handling**:
```python
# Custom error pages
@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    # Log server-side only
    app.logger.error(f"Internal error: {e}")
    return render_template("errors/500.html"), 500
```

**Structured Logging** (instead of debug):
```python
import logging
logging.basicConfig(level=logging.INFO)
# Log to file, not browser
```

### Expected Security Improvement
- No stack traces or source code in HTTP responses
- Generic error pages for users
- Detailed logs retained server-side only
- Debugger PIN never exposed

### Retest Objective
1. Visit `/profile/abc` (invalid ID → ValueError)
2. Observe: Generic error page (no traceback, no source)
3. Verify application logs error server-side
4. Verify no debugger PIN in response or console

---

## T-007: Plaintext Password Storage

### Current Weakness
```python
# app.py:55
password TEXT NOT NULL,   -- plaintext on purpose

# app.py:76-79
INSERT INTO users (username, password, role, email) VALUES
    ('admin', 'admin123', 'admin', 'admin@lab01.local'),
    ('alice', 'alice123', 'user', 'alice@lab01.local'),
    ('bob',   'bob123',   'user', 'bob@lab01.local');
```

### Why Dangerous
- Passwords readable by anyone with DB access or admin panel
- Credential reuse attacks across systems
- Compliance violation (GDPR, PCI-DSS, etc.)
- No defense if database compromised

### Secure Implementation
**Password Hashing with bcrypt** (primary fix):
```python
# secure-examples/auth.py
from werkzeug.security import generate_password_hash, check_password_hash

# Registration / seeding
hashed = generate_password_hash("admin123")  # bcrypt by default
# Store: hashed (e.g., 'scrypt:32768:8:1$...')

# Login verification
row = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
if row and check_password_hash(row['password'], password):
    # Valid credentials
    session["user_id"] = row["id"]
    # ...
```

**Migration Strategy** (for existing plaintext):
```sql
-- Add new column
ALTER TABLE users ADD COLUMN password_hash TEXT;

-- Migrate (one-time script)
UPDATE users SET password_hash = generate_hash(password);
-- Then drop plaintext column after verification
```

**Constant-Time Comparison** (built into `check_password_hash`)

### Expected Security Improvement
- Passwords stored as irreversible hashes
- Even full DB disclosure doesn't reveal passwords
- Meets baseline security compliance requirements

### Retest Objective
1. Inspect `users` table: `SELECT username, password FROM users;`
2. Verify: Password column contains bcrypt hashes (start with `$2b$` or `scrypt:`)
3. Login with valid credentials → Success
4. Login with invalid credentials → Failure
5. Verify admin panel shows hashes, not plaintext

---

## T-008: Static Hardcoded Session Secret

### Current Weakness
```python
# app.py:21
app.secret_key = "lab01-static-secret-key"
```
Static, guessable secret enables offline session forgery.

### Why Dangerous
- Anyone with source code can forge valid session cookies
- Can escalate to admin by forging `{"role": "admin"}`
- CSRF token prediction (if used)
- No rotation — compromise is permanent

### Secure Implementation
**Environment Variable** (primary fix):
```python
# app.py
import os

app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable not set")
```

**Deployment**:
```bash
# .env (not committed)
SECRET_KEY="$(openssl rand -base64 32)"

# Or in systemd/service config
Environment=SECRET_KEY=...
```

**Key Rotation Strategy**:
```python
# Multiple keys for rotation (itsdangerous supports key lists)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SECRET_KEY_FALLBACKS'] = [
    os.environ.get("SECRET_KEY_OLD_1"),
    os.environ.get("SECRET_KEY_OLD_2"),
].filter(None)
```

### Expected Security Improvement
- Secret not in source code
- Unique per deployment
- Rotatable without invalidating all sessions immediately
- Offline forgery impossible without server access

### Retest Objective
1. Restart application
2. Verify new session cookie created (different signature)
3. Verify old sessions invalidated (or gracefully rotated)
4. Verify source code contains no hardcoded secret
5. Verify `SECRET_KEY` loaded from environment

---

## Secure Examples Directory Structure

```
secure-examples/
├── README.md                    # Overview of secure implementations
├── app_secure.py               # Fully secured Flask app
├── auth.py                     # Secure authentication module
├── sanitize.py                 # Input sanitization utilities
├── config.py                   # Secure configuration
├── templates_secure/           # Templates without |safe
│   ├── search.html
│   ├── comments.html
│   └── admin.html
└── requirements-secure.txt     # Additional deps (bcrypt, bleach, etc.)
```

**Note**: These are **educational examples only** — they do not replace the vulnerable `app.py` which must remain for training validation.

---

## Remediation Priority Order

| Priority | Threat | Effort | Risk Reduction |
|----------|--------|--------|----------------|
| 1 | T-005 (Admin Authz) | Low (1 line) | Critical → Medium |
| 2 | T-001 (SQLi Login) | Low (1 line) | High → Low |
| 3 | T-004 (Stored XSS) | Low (1 line) | High → Low |
| 4 | T-002 (IDOR) | Low (3 lines) | High → Low |
| 5 | T-007 (Plaintext PW) | Medium (hashing) | High → Low |
| 6 | T-008 (Static Secret) | Low (env var) | High → Low |
| 7 | T-003 (Reflected XSS) | Low (1 line) | Medium → Low |
| 8 | T-006 (Debug Mode) | Low (1 line) | Medium → Low |

---

## Verification Checklist

After implementing all remediations:

- [ ] All parameterized queries (no string concatenation in SQL)
- [ ] All `|safe` filters removed from templates
- [ ] CSP header implemented and tested
- [ ] Role checks on all privileged endpoints
- [ ] Ownership checks on all user-data endpoints
- [ ] Passwords hashed with bcrypt/scrypt/Argon2
- [ ] `SECRET_KEY` from environment, not source
- [ ] `app.debug = False`
- [ ] Custom error pages (no stack traces)
- [ ] Input validation on all user inputs
- [ ] Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] Retest all T-001 through T-008 → PASS
- [ ] No regressions in legitimate functionality