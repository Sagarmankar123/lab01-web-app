# STRIDE Threat Model Register

## Overview

This register documents the deliberate vulnerabilities in LAB-01 mapped to STRIDE categories, as established in the RabTech Academy dossier Section 4.1. Each threat is derived from actual source code vulnerabilities — no threats are invented beyond what exists in the application.

**Asset**: LAB-01 (Local Training Web App)  
**Scope**: `http://127.0.0.1:8080` — isolated localhost only  
**Methodology**: Manual code review + controlled runtime validation per Rules of Engagement

---

## STRIDE Register

| Threat ID | Asset | Component | STRIDE Category | Threat Description | Preconditions | Impact | Likelihood | Severity | Mitigation |
|-----------|-------|-----------|-----------------|-------------------|---------------|--------|------------|----------|------------|
| T-001 | LAB-01 | `POST /login` | **Tampering** (Primary)<br>**Spoofing** (Secondary) | SQL Injection via string concatenation in authentication query. Username `admin' -- ` bypasses password check. | 1. Access to `/login` endpoint<br>2. Knowledge of valid username (admin) | Authentication bypass; full account takeover; potential data exfiltration via UNION attacks | High (trivial exploit, no auth required) | **High** | Use parameterized queries: `cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))` |
| T-002 | LAB-01 | `GET /profile/<id>` | **Tampering** (Primary)<br>**Information Disclosure** (Secondary) | Insecure Direct Object Reference (IDOR). Application validates session exists but not ownership. Any authenticated user can access `/profile/1`, `/profile/2`, `/profile/3`. | 1. Valid authenticated session (any role)<br>2. Knowledge of target user ID | Horizontal privilege escalation; access to other users' notes and profile data (emails, notes with sensitive info) | High (trivial, authenticated only) | **High** | Add ownership check: `if target['id'] != session['user_id']: return 403`; implement resource-based access control |
| T-003 | LAB-01 | `GET /search?q=` | **Information Disclosure** (Primary)<br>**Tampering** (Secondary) | Reflected Cross-Site Scripting (XSS). Query parameter reflected in response with `\|safe` Jinja2 filter, disabling auto-escaping. Payload: `?q=<script>alert(document.cookie)</script>`. | 1. Victim visits crafted URL<br>2. No CSP header present | Session hijacking (cookie theft); credential harvesting; defacement; malware delivery | Medium (requires victim interaction) | **Medium** | Remove `\|safe` filter; enable Jinja2 autoescape globally; implement CSP header; validate/sanitize input |
| T-004 | LAB-01 | `POST /comments` | **Tampering** (Primary)<br>**Information Disclosure** (Secondary) | Stored Cross-Site Scripting (XSS). Comment content stored in database and rendered with `\|safe` filter for all visitors. Payload executes in every visitor's browser context. | 1. Ability to post comment (any user)<br>2. Victim views `/comments` page | Persistent session hijacking; credential theft; worms; defacement; affects all users including admin | High (persistent, affects all visitors) | **High** | Remove `\|safe` filter; implement output encoding; sanitize on input (allowlist); CSP header |
| T-005 | LAB-01 | `GET /admin` | **Elevation of Privilege** (Primary)<br>**Information Disclosure** (Secondary) | Broken Access Control / Missing Authorization. Route checks for session existence only, never validates `role == 'admin'`. Any logged-in user accesses admin panel with all users' plaintext passwords. | 1. Valid authenticated session (any role)<br>2. Direct navigation to `/admin` | Vertical privilege escalation; full user enumeration; plaintext password disclosure; account takeover | High (trivial, authenticated only) | **Critical** | Add role check: `if session.get('role') != 'admin': return 403`; implement RBAC middleware; hash passwords |
| T-006 | LAB-01 | Application-wide (`app.debug = True`) | **Information Disclosure** | Debug mode enabled. Unhandled exceptions expose full stack traces, source code, and interactive debugger (Werkzeug PIN). Trigger: malformed input (e.g., `/profile/abc`). | 1. Any unhandled exception<br>2. Debug mode active | Source code disclosure; internal architecture exposure; interactive debugger enables RCE if PIN known | Medium (requires error trigger) | **Medium** | Set `app.debug = False` in production; use proper error pages; log errors server-side only |
| T-007 | LAB-01 | Database (`users` table) | **Information Disclosure** (Primary)<br>**Spoofing** (Secondary) | Plaintext password storage. Passwords stored unhashed in `users.password` column. Exposed via `/admin` panel and direct database access. | 1. Access to `/admin` (T-005) or<br>2. Direct database access | Credential reuse across systems; account takeover; password spraying; compliance violation | High (if admin accessed or DB exposed) | **High** | Hash passwords with bcrypt/Argon2/scrypt; never store plaintext; use constant-time comparison |
| T-008 | LAB-01 | Session Management (`app.secret_key`) | **Spoofing** (Primary)<br>**Tampering** (Secondary) | Static hardcoded Flask secret key (`lab01-static-secret-key`). Enables offline session forgery, privilege escalation via crafted cookies, and CSRF token prediction. | 1. Knowledge of secret key (in source code)<br>2. Understanding of Flask session format | Session forgery; privilege escalation (forge admin session); CSRF bypass; impersonation | High (key in source code) | **High** | Use strong random secret per deployment; store in environment variable; rotate periodically; use `itsdangerous` TimestampSigner |

---

## STRIDE Category Summary

| STRIDE | Threat Count | Threat IDs | Highest Severity |
|--------|--------------|------------|------------------|
| **Spoofing** | 2 | T-001 (secondary), T-008 | High |
| **Tampering** | 4 | T-001, T-002, T-003 (secondary), T-004 | High |
| **Repudiation** | 0 | — | — |
| **Information Disclosure** | 5 | T-002 (secondary), T-003, T-004 (secondary), T-005 (secondary), T-006, T-007 | Critical (via T-005) |
| **Denial of Service** | 0 | — | — |
| **Elevation of Privilege** | 1 | T-005 | Critical |

---

## Threat Traceability to Source Code

| Threat ID | File | Line(s) | Code Evidence |
|-----------|------|---------|---------------|
| T-001 | `app.py` | 106-112 | `query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)` |
| T-002 | `app.py` | 136-148 | `if "user_id" not in session:` (line 141) — no ownership check |
| T-003 | `templates/search.html` | 9 | `{{ query\|safe }}` |
| T-004 | `templates/comments.html` | 11 | `{{ c['content']\|safe }}` |
| T-005 | `app.py` | 178-187 | `if "user_id" not in session:` (line 183) — no role check |
| T-006 | `app.py` | 25 | `app.debug = True` |
| T-007 | `app.py` | 55, 76-79 | `password TEXT NOT NULL` — plaintext; `INSERT ... VALUES ('admin', 'admin123', ...)` |
| T-008 | `app.py` | 21 | `app.secret_key = "lab01-static-secret-key"` |

---

## Cross-Reference: Dossier Section 4.1 Mapping

The following table maps each threat to the RabTech Academy dossier Section 4.1 STRIDE table:

| Dossier Row | Route | STRIDE | Priority | This Register |
|-------------|-------|--------|----------|---------------|
| 1 | `POST /login` | Tampering | High | T-001 |
| 2 | `GET /profile/<id>` | Tampering | High | T-002 |
| 3 | `GET /search?q=` | Information Disclosure | Medium | T-003 |
| 4 | `POST /comments` | Tampering / Info Disclosure | High | T-004 |
| 5 | `GET /admin` | Elevation of Privilege | Critical | T-005 |
| 6 | App-wide | Information Disclosure | Medium | T-006 |
| 7 | Database | Information Disclosure | High | T-007 |
| 8 | App-wide | Spoofing | High | T-008 |

**All dossier-identified threats are represented.** No additional threats invented.