# Finding Template

## Instructions

1. Copy this file to `findings/FIND-YYYY-NNN-descriptive-title.md`
2. Fill in all sections completely
3. Reference evidence files in `evidence/`
4. Cross-reference Threat ID (T-XXX) and Test ID (T-XXX)
5. Do not commit until evidence is redacted per `docs/evidence-handling.md`

---

## Finding Header

| Field | Value |
|-------|-------|
| **Finding ID** | FIND-YYYY-NNN (e.g., FIND-2026-001) |
| **Title** | [Concise descriptive title] |
| **Asset** | LAB-01 / LAB-02 |
| **Affected Component** | [Route, component, table, config file] |
| **STRIDE Category** | Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege |
| **Severity** | Critical / High / Medium / Low |
| **Severity Rationale** | [Why this rating: exploitability, impact, scope, privilege required] |
| **CWE** | [CWE-ID if applicable, e.g., CWE-89, CWE-79, CWE-639] |
| **OWASP Top 10** | [Category if applicable, e.g., A03:2021-Injection] |
| **Threat ID** | [From threat-model/stride-register.md, e.g., T-001] |
| **Test ID** | [From testing/test-plan.md, e.g., T-001] |
| **Date Discovered** | YYYY-MM-DD |
| **Assessor** | [Name/ID] |
| **Status** | DRAFT / REVIEWED / CONFIRMED / REMEDIATED / RETESTED / CLOSED |

---

## Description

[Clear, concise description of the vulnerability. What is the flaw? Where does it exist?]

**Example**: The login endpoint (`POST /login`) constructs SQL queries by string concatenation of user-supplied username and password parameters, allowing SQL injection authentication bypass.

---

## Preconditions

[What must be true before the vulnerability can be exploited?]

- [ ] [Precondition 1, e.g., Access to `/login` endpoint]
- [ ] [Precondition 2, e.g., Knowledge of valid username `admin`]
- [ ] [Precondition 3, e.g., Application running with debug mode]

---

## Reproduction Steps

[Numbered, deterministic steps to reproduce the vulnerability. Another tester should be able to follow these exactly.]

1. [Step 1: e.g., Navigate to `http://127.0.0.1:8080/login`]
2. [Step 2: e.g., Enter username `admin' -- ` and password `anything`]
3. [Step 3: e.g., Click "Log in" / Submit form]
4. [Step 4: e.g., Observe redirect to `/dashboard` with admin session]
5. [Step 5: e.g., Visit `/admin` to confirm admin access]

---

## Observed Result

[What actually happened? Include specific observations, not just "it worked."]

**Example**: Application returned HTTP 302 redirect to `/dashboard`. Session cookie set with `user_id=1`, `username=admin`, `role=admin`. Subsequent request to `/admin` returned full user table with plaintext passwords.

---

## Expected Result (Secure Behavior)

[What should happen in a secure implementation?]

**Example**: Login should fail with "Invalid username or password" because parameterized query treats `admin' -- ` as literal username string, not SQL syntax.

---

## Impact

### Confidentiality
[What data can be read? e.g., All user records, plaintext passwords, session tokens]

### Integrity
[What data can be modified? e.g., Authentication bypass, data injection via UNION]

### Availability
[Can service be disrupted? e.g., Potential DoS via heavy queries, database corruption]

### Scope
[Single user / All users / System-wide / Cross-system]

---

## Evidence

[Reference to evidence files in `evidence/` directory. All evidence must be redacted.]

| Evidence File | Description | Redaction Applied |
|---------------|-------------|-------------------|
| `evidence/FIND-YYYY-NNN-01.png` | [e.g., Screenshot of admin dashboard after SQLi login] | [Session cookie, passwords] |
| `evidence/FIND-YYYY-NNN-02.txt` | [e.g., curl request/response log] | [Session cookie] |

---

## Root Cause

[Technical explanation of the underlying code/configuration flaw.]

**Example**: In `app.py` lines 106-112, the login query uses Python string formatting:
```python
query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
```
This allows user input to terminate the string literal and inject arbitrary SQL. The `-- ` sequence comments out the password check.

---

## Remediation

### Specific Fix
[Actionable, code-level remediation. Not generic advice.]

**Example**: Replace string concatenation with parameterized query:
```python
# Vulnerable
query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
row = db.execute(query).fetchone()

# Secure
query = "SELECT * FROM users WHERE username = ? AND password = ?"
row = db.execute(query, (username, password)).fetchone()
```

### Defense in Depth
[Additional mitigations: WAF, input validation, least privilege, etc.]

- [ ] Implement parameterized queries for ALL database interactions
- [ ] Add input validation (allowlist for username: alphanumeric only)
- [ ] Implement account lockout after failed attempts
- [ ] Log failed login attempts (without logging passwords)

### Configuration Changes
[Any config/file changes needed]

- [ ] Ensure `app.debug = False` in production
- [ ] Use environment variable for `SECRET_KEY`

---

## Retest

### Retest Objective
[Specific, verifiable test to confirm fix works.]

**Example**: Submit `admin' -- ` as username with any password → login fails → returns "Invalid username or password"

### Retest Date
YYYY-MM-DD

### Retest Status
NOT TESTED / PASS / FAIL / PARTIAL

### Retest Evidence
| Evidence File | Description |
|---------------|-------------|
| `evidence/FIND-YYYY-NNN-retest-01.png` | [Screenshot of failed login attempt] |

### Residual Risk
[Any remaining risk after fix? e.g., "None — parameterized queries eliminate SQLi in this endpoint"]

---

## References

- [ ] `threat-model/stride-register.md` — Threat ID: T-XXX
- [ ] `testing/test-plan.md` — Test ID: T-XXX
- [ ] `testing/test-results.md` — Execution record
- [ ] CWE-XXX: [Link or description]
- [ ] OWASP Top 10 2021: Axx: [Category]
- [ ] RabTech Dossier Section 4.1: [Row reference]

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Assessor | | | |
| Reviewer | | | |
| Lab Owner | | | |