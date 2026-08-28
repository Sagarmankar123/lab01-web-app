# Test Plan

## Overview

This test plan maps each known vulnerability in LAB-01 to a controlled validation objective. Tests are designed for manual, low-rate execution per the Rules of Engagement and Testing Methodology.

**Asset**: LAB-01 (`http://127.0.0.1:8080`)  
**Tester**: [Assessor Name]  
**Window**: [Approved window — To be completed]  
**Baseline**: Fresh lab state (post `/reset-lab`)

---

## Test Cases

| Test ID | Asset | Route/Component | Objective | Preconditions | Test Steps | Expected Evidence | Status |
|---------|-------|-----------------|-----------|---------------|------------|-------------------|--------|
| T-001 | LAB-01 | `POST /login` | Validate SQL injection authentication bypass | Lab reset; app running | 1. GET `/login`<br>2. POST username=`admin' -- `, password=`x`<br>3. Observe redirect to `/dashboard` | Screenshot: dashboard as admin; session cookie | NOT EXECUTED |
| T-002 | LAB-01 | `GET /profile/<id>` | Validate IDOR — unauthorized profile access | Valid user session (alice) | 1. Login as alice/alice123<br>2. GET `/profile/1` (admin)<br>3. GET `/profile/3` (bob)<br>4. Observe profile data + notes | Screenshots: admin profile, bob profile (redacted) | NOT EXECUTED |
| T-003 | LAB-01 | `GET /search?q=` | Validate reflected XSS via search parameter | None (pre-auth) | 1. GET `/search?q=<script>alert('XSS')</script>`<br>2. Observe script execution<br>3. Verify no CSP block | Screenshot: alert dialog + URL in address bar | NOT EXECUTED |
| T-004 | LAB-01 | `POST /comments` | Validate stored XSS persistence & cross-user execution | Lab reset; app running | 1. GET `/comments`<br>2. POST author=`test`, content=`<script>alert('Stored')</script>`<br>3. Observe execution in same session<br>4. Open incognito, visit `/comments`<br>5. Observe execution for new visitor | Screenshots: same session + incognito (2) | NOT EXECUTED |
| T-005 | LAB-01 | `GET /admin` | Validate missing role check — vertical privilege escalation | Valid user session (alice) | 1. Login as alice/alice123<br>2. GET `/admin` directly<br>3. Observe full user table with plaintext passwords | Screenshot: admin panel (passwords redacted) | NOT EXECUTED |
| T-006 | LAB-01 | Error handling | Validate debug mode information disclosure | None (pre-auth) | 1. GET `/profile/abc` (invalid ID)<br>2. Observe Werkzeug traceback<br>3. Verify source code exposure | Screenshot: traceback (paths redacted) | NOT EXECUTED |
| T-007 | LAB-01 | Database | Validate plaintext password storage | Admin access (via T-005) OR direct DB | Option A: Via T-005 admin panel<br>Option B: `sqlite3 lab01.db "SELECT username, password FROM users;"` | Screenshot/query output: password column (values redacted) | NOT EXECUTED |
| T-008 | LAB-01 | Session config | Assess static secret key configuration | Source code access | 1. Inspect `app.py` line 21<br>2. Verify `app.secret_key = "lab01-static-secret-key"`<br>3. (Optional offline) Demonstrate session forgery with itsdangerous | Screenshot: source code line 21 | NOT EXECUTED |

---

## LAB-02 Test Cases (Conditional)

*Only execute if explicitly authorized by lab owner with defined scope.*

| Test ID | Asset | Target | Objective | Preconditions | Test Steps | Expected Evidence | Status |
|---------|-------|--------|-----------|---------------|------------|-------------------|--------|
| T-009 | LAB-02 | Host-only network | Verify network isolation | Host-only adapter configured | 1. Ping `192.168.56.20`<br>2. Verify no route to internet<br>3. Verify no route to `127.0.0.1` | Ping output; route table | NOT EXECUTED |
| T-010 | LAB-02 | Service enumeration | Identify listening services | Explicit authorization | 1. Single SYN scan authorized ports<br>2. Banner grab responsive ports | Scan output; banners (redacted) | NOT EXECUTED |

---

## Test Execution Order

**Required Sequence** (dependencies noted):

1. **T-001** (SQLi Login) — Establishes admin access for T-005, T-007
2. **T-005** (Admin Authz) — Requires authenticated session (any user)
3. **T-007** (Plaintext Passwords) — Requires T-005 or direct DB
4. **T-002** (IDOR) — Requires authenticated session (any user)
5. **T-003** (Reflected XSS) — No preconditions
6. **T-004** (Stored XSS) — Requires lab reset after T-002/T-005
7. **T-006** (Debug Mode) — No preconditions
8. **T-008** (Static Secret) — No preconditions (source review)

**Lab Reset Points**:
- After T-001 (if admin session affects other tests)
- After T-004 (stored XSS persists)
- Before any retest

---

## Evidence Requirements

| Test ID | Evidence Type | Redaction | Storage Path |
|---------|---------------|-----------|--------------|
| T-001 | Screenshot (dashboard + URL) | Session cookie | `evidence/T-001-dashboard.png` |
| T-002 | Screenshots (2 profiles) | Emails, notes | `evidence/T-002-profile-1.png`, `evidence/T-002-profile-3.png` |
| T-003 | Screenshot (alert + URL) | None needed | `evidence/T-003-search-xss.png` |
| T-004 | Screenshots (2 contexts) | None needed | `evidence/T-004-stored-same.png`, `evidence/T-004-stored-incognito.png` |
| T-005 | Screenshot (admin table) | **Passwords**, emails | `evidence/T-005-admin-panel.png` |
| T-006 | Screenshot (traceback) | File paths | `evidence/T-006-debug-traceback.png` |
| T-007 | Screenshot or query output | **Password values** | `evidence/T-007-plaintext-passwords.png` |
| T-008 | Screenshot (source code) | None needed | `evidence/T-008-static-secret.png` |

---

## Success Criteria

| Test ID | Pass Criteria | Fail Criteria |
|---------|---------------|---------------|
| T-001 | Login succeeds as admin with SQLi payload | Login fails (parameterized query) |
| T-002 | Other users' profiles accessible | 403/404 for unauthorized profiles |
| T-003 | Script executes in browser | Script rendered as text (escaped) |
| T-004 | Script executes for all visitors | Script rendered as text (escaped) |
| T-005 | Admin panel accessible as non-admin | 403 Forbidden for non-admin |
| T-006 | Traceback with source shown | Generic error page |
| T-007 | Passwords visible in plaintext | Passwords hashed (bcrypt) |
| T-008 | Secret is static string in source | Secret from env var, rotates |

---

## Resource Requirements

- **Tools**: Browser (Firefox/Chrome), curl, SQLite3 CLI, Python 3.11+
- **Environment**: Windows/PowerShell (as used), venv activated
- **Network**: Localhost only; host-only adapter for LAB-02
- **Time**: Estimated 2-3 hours for full LAB-01 test cycle

---

## Risk Mitigation During Testing

| Risk | Mitigation |
|------|------------|
| Accidental data loss | Use `/reset-lab` before/after; no destructive payloads |
| Session confusion | Use incognito/private windows for cross-user tests |
| Evidence contamination | Redact immediately; store in `evidence/` only |
| Scope creep | Refer to test plan; no ad-hoc exploration beyond defined tests |
| LAB-02 impact | Do not test LAB-02 unless explicitly authorized |