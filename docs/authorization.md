# Authorization Document

## Project Information

| Field | Value |
|-------|-------|
| **Project Name** | RabTech Academy — Task 02: Legal Scope, Asset Inventory & Threat Model |
| **Lab Owner** | RabTech Academy |
| **Assessor** | [Student Name / ID — To be completed by lab owner] |
| **Purpose** | Authorized security assessment of intentionally vulnerable training assets (LAB-01 and LAB-02) for educational threat modeling and vulnerability validation |
| **Approval Date** | [To be completed by lab owner] |
| **Authorization Reference** | [To be completed by lab owner — e.g., RABTECH-T02-AUTH-XXXX] |

---

## Authorized Assets

### LAB-01 — Local Training Web App
- **Asset ID**: LAB-01
- **Name**: Local training web app
- **Owner**: RabTech lab
- **Environment**: Isolated localhost
- **URL**: `http://127.0.0.1:8080`
- **Testing**: Allowed (manual, low-rate, non-destructive only)
- **Exclusions**: No denial of service, no third-party scanning, no automated credential stuffing
- **Evidence Classification**: Confidential training evidence

### LAB-02 — Deliberately Vulnerable VM
- **Asset ID**: LAB-02
- **Name**: Deliberately vulnerable VM
- **Owner**: RabTech lab
- **Environment**: Private host-only network
- **IP**: `192.168.56.20`
- **Testing**: Allowed (manual, low-rate, non-destructive only)
- **Exclusions**: No persistence, no outbound traffic, no pivoting
- **Evidence Classification**: Confidential training evidence

---

## Scope

### In Scope
- LAB-01 web application at `http://127.0.0.1:8080`
  - All routes: `/`, `/login`, `/logout`, `/dashboard`, `/profile/<id>`, `/search`, `/comments`, `/admin`, `/reset-lab`
  - SQLite database (`lab01.db`) interactions
  - Session management and authentication flows
  - Input validation and output encoding behavior
- LAB-02 VM at `192.168.56.20` (host-only network)
  - Network-level reconnaissance (passive only)
  - Service enumeration on approved ports
  - Configuration review

### Out of Scope
- Any system not explicitly listed above
- College/university networks
- Public internet targets
- GitHub.com or any code hosting platform (publication only, not testing)
- Personal devices
- Third-party servers or services
- Any asset reachable via public IP
- Denial-of-service testing
- Load testing
- Automated vulnerability scanning at scale
- Credential stuffing or brute-force attacks
- Persistence mechanisms
- Outbound traffic generation from LAB-02
- Pivoting from LAB-01 or LAB-02 to other hosts
- Social engineering
- Physical security testing

---

## Testing Window

**Approved Window**: [Student-defined approved window — To be completed by lab owner]

Testing must only occur within the approved window. Any testing outside this window is unauthorized.

---

## Stop Conditions

Testing must cease immediately if any of the following occur:

1. Target system is outside the authorized asset inventory
2. Unexpected third-party system is reached or contacted
3. Outbound traffic originates from LAB-02
4. Lab environment becomes unstable or unresponsive
5. Unexpected sensitive data (real credentials, PII, production data) is exposed
6. Evidence collection exceeds approved scope
7. Lab owner or instructor instructs testing to stop
8. Any indicator of compromise on systems outside the lab
9. Network connectivity to unauthorized networks is detected

---

## Evidence Classification

All evidence collected during this assessment is classified as **Confidential Training Evidence**.

### Handling Requirements
- Evidence must not leave the controlled lab environment
- Evidence must be redacted per `docs/evidence-handling.md` before any storage or sharing
- Raw evidence must be deleted within [To be defined by lab owner] after assessment completion
- Only minimum necessary evidence to substantiate findings may be retained
- No real credentials, API keys, tokens, or personal data may be committed to version control

---

## Authorization Statement

> "I, [Lab Owner Name], authorize [Assessor Name] to conduct manual, low-rate, non-destructive security testing against LAB-01 (`http://127.0.0.1:8080`) and LAB-02 (`192.168.56.20`) within the approved window defined above. This authorization is limited to the scope, exclusions, and stop conditions documented herein."

**Lab Owner Signature**: _________________________  **Date**: _______________

**Assessor Acknowledgment**: _____________________  **Date**: _______________