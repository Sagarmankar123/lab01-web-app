# Evidence Directory

## Purpose

This directory stores all evidence captured during the authorized security assessment. Evidence is classified as **Confidential Training Evidence** per `docs/authorization.md`.

## Directory Structure

```
evidence/
├── README.md           # This file — evidence index
├── .gitkeep           # Keeps directory in git
├── FIND-2026-001-*.png    # Redacted evidence for findings (tracked)
├── FIND-2026-002-*.png
└── raw/               # Raw/unredacted evidence (GITIGNORED)
    ├── .gitkeep
    └── *.png, *.txt, *.pcap
```

## Evidence Handling Rules

### Before Storing ANY Evidence

**MANDATORY REDACTION** — Apply to every file:

| Data Type | Redaction | Example |
|-----------|-----------|---------|
| Passwords (plaintext) | `[REDACTED]` | `admin123` → `[REDACTED]` |
| Passwords (hashed) | `[REDACTED]` | `$2b$12$...` → `[REDACTED]` |
| Session cookies | `[REDACTED]` | `session=abc123` → `session=[REDACTED]` |
| CSRF tokens | `[REDACTED]` | `csrf_token=xyz` → `csrf_token=[REDACTED]` |
| API keys / secrets | `[REDACTED]` | `sk_live_...` → `[REDACTED]` |
| Werkzeug debugger PIN | `[REDACTED]` | `143-264-480` → `[REDACTED]` |
| Real emails (PII) | `[REDACTED]` | `user@domain.com` → `[REDACTED]` |
| Real names (PII) | `[REDACTED]` | `John Doe` → `[REDACTED]` |
| Internal file paths | `[REDACTED]` | `/home/user/app.py` → `[REDACTED]` |
| Non-lab IP addresses | `[REDACTED]` | `10.0.0.5` → `[REDACTED]` |

**Training data exceptions** (may remain unredacted with note):
- Seeded accounts: `admin`, `alice`, `bob` (usernames)
- Training emails: `admin@lab01.local`, `alice@lab01.local`, `bob@lab01.local`
- Lab IPs: `127.0.0.1:8080`, `192.168.56.20`

### Evidence Capture Standards

| Type | Format | Max Size | Naming |
|------|--------|----------|--------|
| Screenshots | PNG | 1920x1080 | `FIND-YYYY-NNN-description.png` |
| Request/Response | Text (curl -v) | 100 KB | `FIND-YYYY-NNN-reqres.txt` |
| Database queries | Text | 50 KB | `FIND-YYYY-NNN-query.txt` |
| Network captures | PCAP | 10 MB | `FIND-YYYY-NNN-capture.pcap` |
| Configuration | Text/Code | 50 KB | `FIND-YYYY-NNN-config.txt` |

### Evidence Index

*All evidence files must be listed here with finding references.*

| File | Finding ID | Test ID | Description | Redacted | Date |
|------|------------|---------|-------------|----------|------|
| — | — | — | No evidence captured yet | — | — |

### Retention & Deletion

| Evidence Type | Retention | Deletion Trigger |
|---------------|-----------|------------------|
| Raw evidence (`evidence/raw/`) | [To be defined by lab owner — e.g., 30 days] | Assessment completion + retention period |
| Processed evidence (`evidence/*.png`) | Academic record duration | Course completion + [To be defined] |
| Finding-linked evidence | Same as finding | Finding CLOSED + retention period |

**Deletion Procedure**:
1. Verify finding status = CLOSED
2. Verify retention period elapsed
3. Secure delete (shred/srm) raw evidence
4. Remove processed evidence from git history (if required)
5. Update this index

### Chain of Custody

For formal assessments, record:

| Evidence File | Captured By | Date/Time | Hash (SHA256) | Transferred To | Date/Time |
|---------------|-------------|-----------|---------------|----------------|-----------|
| — | — | — | — | — | — |

---

## Prohibited Evidence

**NEVER store in this repository**:
- [ ] Real production credentials
- [ ] Real API keys / tokens / certificates
- [ ] Real PII (non-training)
- [ ] Malware samples
- [ ] Exploit code / weapons
- [ ] Large data dumps (>10 MB)
- [ ] Unredacted screenshots
- [ ] Evidence from unauthorized targets

---

## Access Control

- This directory is part of the git repository
- `evidence/raw/` is in `.gitignore` — never committed
- Only authorized assessor and lab owner should access
- No evidence shared outside approved channels

---

## Attestation

> "All evidence in this directory has been captured per the Rules of Engagement, redacted per the evidence handling procedures, and is associated with a documented finding. No unauthorized evidence is present."

**Assessor**: _________________________  **Date**: _______________

**Lab Owner**: _________________________  **Date**: _______________