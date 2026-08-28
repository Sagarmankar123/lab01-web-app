# Findings Directory

## Purpose

This directory contains individual finding reports for each confirmed vulnerability. Each finding follows the standardized template in `finding-template.md`.

## Finding Index

*Populated as findings are confirmed during testing.*

| Finding ID | Title | Asset | Severity | Status | Test ID | Evidence |
|------------|-------|-------|----------|--------|---------|----------|
| — | — | — | — | — | — | No findings yet |

## Finding Lifecycle

```text
DRAFT → REVIEWED → CONFIRMED → REMEDIATED → RETESTED → CLOSED
```

### Status Definitions

| Status | Meaning |
|--------|---------|
| **DRAFT** | Initial documentation; evidence being gathered |
| **REVIEWED** | Peer/instructor review complete |
| **CONFIRMED** | Vulnerability validated; evidence accepted |
| **REMEDIATED** | Fix applied in secure-examples/ or separate branch |
| **RETESTED** | Retest performed; fix verified |
| **CLOSED** | Final sign-off; no residual risk |

## File Naming Convention

```
findings/FIND-YYYY-NNN-descriptive-title.md
```

Examples:
- `findings/FIND-2026-001-sqli-login-auth-bypass.md`
- `findings/FIND-2026-002-idor-profile-access.md`
- `findings/FIND-2026-003-reflected-xss-search.md`
- `findings/FIND-2026-004-stored-xss-comments.md`
- `findings/FIND-2026-005-broken-authz-admin-panel.md`
- `findings/FIND-2026-006-debug-mode-disclosure.md`
- `findings/FIND-2026-007-plaintext-password-storage.md`
- `findings/FIND-2026-008-static-session-secret.md`

## Evidence References

Each finding must reference evidence files in `evidence/`:
- Format: `evidence/FIND-YYYY-NNN-description.png`
- Multiple evidence files allowed per finding
- All evidence must be redacted per `docs/evidence-handling.md`

## Cross-References

Each finding should reference:
- **Threat ID** from `threat-model/stride-register.md` (T-001 through T-008)
- **Test ID** from `testing/test-plan.md` (T-001 through T-008)
- **Retest ID** from `testing/test-results.md` (after remediation)
- **CWE** identifiers where applicable
- **OWASP Top 10** category where applicable

## Review Process

1. Assessor drafts finding during/after validation
2. Finding reviewed for completeness (all template fields)
3. Evidence verified for redaction compliance
4. Finding marked CONFIRMED or returned for revision
5. After remediation, retest conducted
6. Finding marked RETESTED → CLOSED

## Confidentiality

All findings are **Confidential Training Evidence** per `docs/authorization.md`. Do not share outside authorized channels.