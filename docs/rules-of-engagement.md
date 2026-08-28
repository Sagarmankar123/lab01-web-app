# Rules of Engagement

## 1. Written Authorization

| Field | Value |
|-------|-------|
| **Lab Owner** | RabTech Academy |
| **Assessor** | [Student Name / ID — To be completed by lab owner] |
| **Approved Assets** | LAB-01 (`http://127.0.0.1:8080`), LAB-02 (`192.168.56.20`) |
| **Authorization Reference** | [To be completed by lab owner — e.g., RABTECH-T02-AUTH-XXXX] |
| **Approval Date** | [To be completed by lab owner] |
| **Authorization Scope** | This document and `docs/authorization.md` |

> **Authorization Statement**: "I, [Lab Owner Name], authorize [Assessor Name] to conduct manual, low-rate, non-destructive security testing against LAB-01 and LAB-02 within the approved window, scope, exclusions, and stop conditions defined herein."

**Lab Owner Signature**: _________________________  **Date**: _______________

**Assessor Acknowledgment**: _____________________  **Date**: _______________

---

## 2. Permitted Techniques

Only the following controlled activities are authorized:

### Reconnaissance & Enumeration
- [x] Manual route enumeration (browser, curl)
- [x] Application functionality walkthrough
- [x] Technology fingerprinting (headers, error pages, source inspection)
- [x] Passive network observation (host-only network)

### Authentication Testing
- [x] Valid credential login (seeded accounts)
- [x] Invalid credential testing
- [x] SQL injection authentication bypass validation
- [x] Session cookie inspection (no forgery in production context)

### Authorization Testing
- [x] IDOR validation (profile ID manipulation)
- [x] Vertical privilege escalation (admin panel access)
- [x] Horizontal privilege escalation (other users' data)
- [x] Role-based access verification

### Input Validation Testing
- [x] Reflected XSS payload delivery (search, low-rate)
- [x] Stored XSS payload delivery (comments, single test payload)
- [x] SQL injection payload testing (login, parameterized)
- [x] Path traversal attempts (profile ID parameter)

### Configuration Review
- [x] Debug mode verification
- [x] Secret key inspection (source code)
- [x] Password storage review (database inspection)
- [x] Security header analysis (CSP, HSTS, etc.)

### Evidence Collection
- [x] Screenshots (redacted per evidence handling)
- [x] Request/response logging (redacted)
- [x] Configuration evidence capture
- [x] Assessment notes

### Reporting
- [x] Finding documentation per template
- [x] Risk analysis and severity rating
- [x] Remediation recommendations
- [x] Retest verification

---

## 3. Explicit Exclusions

The following activities are **PROHIBITED** and constitute violation of this engagement:

### Denial of Service & Disruption
- [ ] Any DoS, DDoS, or resource exhaustion testing
- [ ] Large-volume request flooding
- [ ] Application crash induction (beyond single error trigger for debug validation)
- [ ] Database corruption or deletion (except `/reset-lab` for lab reset)

### Destructive Actions
- [ ] Data destruction, modification, or exfiltration beyond minimum evidence
- [ ] Persistence mechanisms (backdoors, webshells, scheduled tasks)
- [ ] Malware deployment or execution
- [ ] File system modification outside application scope

### Credential & Access Abuse
- [ ] Credential stuffing or brute-force at scale
- [ ] Password spraying against seeded accounts (beyond single validation)
- [ ] Credential reuse against external systems
- [ ] Session forgery outside controlled validation (T-008)

### Network & Pivoting
- [ ] Outbound traffic generation from LAB-02
- [ ] Pivoting from LAB-01 to LAB-02 or vice versa
- [ ] Scanning of networks beyond host-only subnet
- [ ] ARP spoofing, DNS poisoning, or MITM on host-only network
- [ ] Access to `127.0.0.1` from LAB-02 or external networks

### Third-Party & External
- [ ] Testing of any system not in asset inventory
- [ ] GitHub.com or code repository testing (publication only)
- [ ] College/university network scanning
- [ ] Public internet target scanning
- [ ] Third-party API or service interaction

### Automation
- [ ] Automated vulnerability scanners (Nessus, OpenVAS, Burp Scanner, etc.)
- [ ] Automated fuzzing tools (ffuf, wfuzz at scale)
- [ ] Credential stuffing automation
- [ ] Any tool generating >10 requests/second sustained

### Social & Physical
- [ ] Social engineering (phishing, vishing, impersonation)
- [ ] Physical security testing
- [ ] Shoulder surfing or device theft

---

## 4. Testing Window

**Approved Window**: [Student-defined approved window — To be completed by lab owner]

- Testing **must only occur** within this window
- Any activity outside this window is **unauthorized**
- Window must be communicated to lab owner before testing begins
- Extensions require written approval

---

## 5. Stop Conditions

Testing must **cease immediately** if any of the following occur:

| # | Stop Condition | Action |
|---|----------------|--------|
| 1 | Target system outside authorized inventory | Stop; document; report to lab owner |
| 2 | Unexpected third-party system reached | Stop; document network path; report |
| 3 | Outbound traffic from LAB-02 detected | Stop; capture evidence; report immediately |
| 4 | Lab environment unstable/unresponsive | Stop; do not force; report |
| 5 | Unexpected sensitive data exposed (real PII, production creds) | Stop; do not capture; report immediately |
| 6 | Evidence collection exceeds approved scope | Stop; purge excess; report |
| 7 | Lab owner/instructor instructs stop | Stop immediately; preserve state |
| 8 | Indicator of compromise outside lab | Stop; isolate; report |
| 9 | Network connectivity to unauthorized networks | Stop; document; report |
| 10 | Assessment scope creep detected | Stop; realign to authorized scope |

**Post-Stop Procedure**:
1. Document exact time and condition
2. Preserve current evidence state
3. Notify lab owner within 1 hour
4. Await written direction to resume or conclude

---

## 6. Evidence Handling

### Minimum Necessary Principle
- Capture only evidence required to substantiate findings
- No full database dumps, no full session captures, no unnecessary screenshots
- One representative screenshot per finding type maximum

### Redaction Requirements
**Before any evidence storage or sharing**:
- [ ] Passwords (plaintext or hashed) → `[REDACTED]`
- [ ] Session cookies / tokens → `[REDACTED]`
- [ ] API keys, secrets, signing keys → `[REDACTED]`
- [ ] Personal identifiable information (emails, names) → `[REDACTED]` or pseudonymized
- [ ] Internal IP addresses (except documented lab IPs) → `[REDACTED]`
- [ ] Werkzeug debugger PIN → `[REDACTED]`

### Secret Handling
- **Never** commit secrets to version control
- **Never** share secrets in chat, email, or unencrypted channels
- Store evidence in `evidence/` directory (gitignored for raw evidence)
- Use `evidence/README.md` for evidence index with finding references

### Personal Data Handling
- Seeded training accounts (admin, alice, bob) are **training data** — may be documented as such
- No real personal data exists in lab — if discovered, treat as Stop Condition #5

### Storage & Retention
- Evidence stored in `evidence/` (tracked in git) and `evidence/raw/` (gitignored)
- Raw evidence deleted within **[To be defined by lab owner — e.g., 30 days]** after assessment
- Processed/redacted evidence retained in findings for academic record
- No evidence leaves the controlled lab environment

---

## 7. Reporting Requirements

Every finding must contain:

| Field | Description |
|-------|-------------|
| **Asset** | LAB-01 or LAB-02 |
| **Finding ID** | Format: `FIND-YYYY-NNN` (e.g., `FIND-2026-001`) |
| **Severity** | Critical / High / Medium / Low |
| **Severity Rationale** | Why this rating (exploitability, impact, scope) |
| **Affected Component** | Route, component, database table, config |
| **Reproduction Steps** | Numbered, deterministic steps |
| **Impact** | Confidentiality, Integrity, Availability impact |
| **Evidence** | Reference to `evidence/` files (redacted) |
| **Root Cause** | Code/configuration flaw |
| **Remediation** | Specific, actionable fix |
| **Retest Status** | NOT TESTED / PASS / FAIL / PARTIAL |
| **References** | CWE, OWASP, dossier section |

### Reporting Timeline
- **Draft findings**: Within 24 hours of validation
- **Final report**: Within approved window + 48 hours
- **Retest report**: Within 24 hours of remediation deployment

---

## 8. Communication & Escalation

| Channel | Purpose | Contact |
|---------|---------|---------|
| **Primary** | Routine coordination | [Lab owner contact — To be completed] |
| **Emergency** | Stop conditions, critical findings | [Lab owner emergency contact — To be completed] |
| **Documentation** | Findings, evidence, reports | This repository (`findings/`, `evidence/`) |

**Escalation Path**:
1. Assessor → Lab Owner (immediate for stop conditions)
2. Lab Owner → RabTech Academy (if policy decision needed)
3. All communications logged with timestamps

---

## 9. Compliance & Attestation

By conducting testing under this RoE, the assessor attests:

> "I have read, understood, and agree to comply with all provisions of this Rules of Engagement document. I will test only the authorized assets within the approved window using only permitted techniques. I will cease testing immediately upon any stop condition. I will handle all evidence per the evidence handling procedures. I will not disclose lab details, vulnerabilities, or evidence outside the authorized reporting channels."

**Assessor Signature**: _________________________  **Date**: _______________

**Lab Owner Acceptance**: _______________________  **Date**: _______________