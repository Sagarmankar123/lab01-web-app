# Test Results

## Overview

This document records the execution results of the test plan defined in `testing/test-plan.md`. All tests are initially marked **NOT EXECUTED** until actual evidence is captured during the approved testing window.

**Status Legend**:
- **NOT EXECUTED**: Test not yet performed
- **PASS**: Vulnerability confirmed; evidence captured
- **FAIL**: Vulnerability not present (mitigated)
- **PARTIAL**: Partial confirmation; limited evidence
- **BLOCKED**: Cannot execute due to dependency/environment

---

## LAB-01 Test Results

| Test ID | Asset | Route/Component | Status | Execution Date | Evidence Reference | Finding ID | Notes |
|---------|-------|-----------------|--------|----------------|-------------------|------------|-------|
| T-001 | LAB-01 | `POST /login` (SQLi) | NOT EXECUTED | — | — | — | Requires approved window |
| T-002 | LAB-01 | `GET /profile/<id>` (IDOR) | NOT EXECUTED | — | — | — | Requires T-001 or valid login |
| T-003 | LAB-01 | `GET /search?q=` (Reflected XSS) | NOT EXECUTED | — | — | — | Pre-auth; no dependencies |
| T-004 | LAB-01 | `POST /comments` (Stored XSS) | NOT EXECUTED | — | — | — | Requires lab reset after |
| T-005 | LAB-01 | `GET /admin` (Broken Authz) | NOT EXECUTED | — | — | — | Requires valid session |
| T-006 | LAB-01 | Error handling (Debug) | NOT EXECUTED | — | — | — | Pre-auth; no dependencies |
| T-007 | LAB-01 | Database (Plaintext PW) | NOT EXECUTED | — | — | — | Requires T-005 or direct DB |
| T-008 | LAB-01 | Session (Static Secret) | NOT EXECUTED | — | — | — | Source review only |

---

## LAB-02 Test Results (Conditional)

| Test ID | Asset | Target | Status | Execution Date | Evidence Reference | Finding ID | Notes |
|---------|-------|--------|--------|----------------|-------------------|------------|-------|
| T-009 | LAB-02 | Network isolation | NOT EXECUTED | — | — | — | Requires explicit authorization |
| T-010 | LAB-02 | Service enumeration | NOT EXECUTED | — | — | — | Requires explicit authorization |

---

## Execution Log

*Record each test execution here with timestamp and outcome.*

| Timestamp | Test ID | Action | Outcome | Evidence Captured |
|-----------|---------|--------|---------|-------------------|
| — | — | No tests executed yet | — | — |

---

## Evidence Index

*All evidence files should be listed here with finding references.*

| Evidence File | Test ID | Finding ID | Description | Redacted |
|---------------|---------|------------|-------------|----------|
| — | — | — | No evidence captured yet | — |

---

## Retest Results

*After remediation, retest results are recorded here.*

| Test ID | Finding ID | Retest Date | Retest Status | Residual Risk | Notes |
|---------|------------|-------------|---------------|---------------|-------|
| — | — | — | — | — | No retests performed |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Tests Planned (LAB-01) | 8 |
| Executed | 0 |
| Passed (Vuln Confirmed) | 0 |
| Failed (Mitigated) | 0 |
| Partial | 0 |
| Blocked | 0 |
| Not Executed | 8 |
| **Total Tests Planned (LAB-02)** | 2 |
| Executed (LAB-02) | 0 |

---

## Notes

1. **No tests have been executed** — this document is initialized for the approved testing window.
2. All tests are **NOT EXECUTED** pending:
   - Signed Rules of Engagement
   - Approved testing window
   - Lab owner authorization
3. Evidence will be captured per `docs/evidence-handling.md` and `docs/testing-methodology.md`
4. Findings will be documented per `findings/finding-template.md`
5. LAB-02 tests remain **NOT EXECUTED** unless explicitly authorized

---

## Attestation

> "I attest that all recorded test results accurately reflect the observed behavior during the approved testing window. No tests were executed outside the authorized scope, window, or techniques. All evidence has been handled per the evidence handling procedures."

**Assessor**: _________________________  **Date**: _______________

**Lab Owner Review**: ___________________  **Date**: _______________