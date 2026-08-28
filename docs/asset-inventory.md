# Asset Inventory

## Asset Register

| Asset ID | Asset | Owner | Environment | Address | Testing | Exclusions | Evidence Classification |
|----------|-------|-------|-------------|---------|---------|------------|------------------------|
| LAB-01 | Local training web app | RabTech lab | Isolated localhost | `http://127.0.0.1:8080` | Allowed (manual, low-rate, non-destructive) | No DoS, no third-party scanning, no automated credential stuffing | Confidential training evidence |
| LAB-02 | Deliberately vulnerable VM | RabTech lab | Private host-only network | `192.168.56.20` | Allowed (manual, low-rate, non-destructive) | No persistence, no outbound traffic, no pivoting | Confidential training evidence |

---

## Asset Purpose

### LAB-01 — Local Training Web App
LAB-01 is an intentionally vulnerable Flask web application designed for authorized cybersecurity training. It serves as the primary target for:
- Threat modeling exercises (STRIDE)
- Vulnerability validation (SQL injection, IDOR, XSS, broken access control, information disclosure)
- Evidence collection and reporting practice
- Remediation guidance development

The application is deliberately seeded with known vulnerabilities mapped to STRIDE categories and priorities per the RabTech Academy dossier Section 4.1.

### LAB-02 — Deliberately Vulnerable VM
LAB-02 is a deliberately vulnerable virtual machine hosted on a private host-only network. It serves as:
- A secondary target for network-level reconnaissance practice
- Service enumeration and configuration review exercises
- Demonstration of host-only network isolation boundaries

**Note**: Specific services, operating system, and vulnerabilities for LAB-02 are NOT VERIFIED in this documentation. Only the network address and isolation boundary are confirmed.

---

## Attack Surface

### LAB-01 Attack Surface (Verified from Source Code)

| Surface | Component | Description | Risk Context |
|---------|-----------|-------------|--------------|
| **Authentication** | `POST /login` | Username/password form with string-built SQL query | SQL injection (Tampering/High) |
| **Authorization** | `GET /profile/<id>` | User profile access with ID parameter, no ownership check | IDOR (Tampering/High) |
| **Input Reflection** | `GET /search?q=` | Query parameter reflected in response with `\|safe` filter | Reflected XSS (Information Disclosure/Medium) |
| **Stored Input** | `POST /comments` | Comment content stored and rendered with `\|safe` filter | Stored XSS (Tampering/Information Disclosure/High) |
| **Privilege Boundary** | `GET /admin` | Admin panel checks session only, not role | Elevation of Privilege (Critical) |
| **Error Handling** | Application-wide | `debug=True` enables interactive debugger and stack traces | Information Disclosure (Medium) |
| **Data Storage** | SQLite database | Passwords stored in plaintext, visible via `/admin` | Information Disclosure (High) |
| **Session Management** | Flask session | Static hardcoded `secret_key` enables session forgery | Spoofing (High) |

**Technology Stack** (from source):
- Flask 3.0.x (Python)
- SQLite 3 (embedded database)
- Jinja2 templating (with `\|safe` usage creating XSS)
- Werkzeug development server (debug mode enabled)

**Network Exposure**: Bound to `127.0.0.1:8080` only — not accessible from network.

### LAB-02 Attack Surface

| Surface | Status | Notes |
|---------|--------|-------|
| Network services | NOT VERIFIED | Host-only network at `192.168.56.20` — specific ports/services not enumerated in this documentation |
| Operating system | NOT VERIFIED | OS type/version not confirmed |
| Web applications | NOT VERIFIED | No web applications confirmed on LAB-02 |
| Remote access | NOT VERIFIED | SSH/RDP/other remote access not confirmed |

**Only confirmed facts**:
- IP address: `192.168.56.20`
- Network: Host-only (VirtualBox/VMware host-only adapter)
- No outbound internet access (by design)
- Isolated from LAB-01 (different network boundaries)

---

## Asset Relationships

```text
Assessment Host (Student Machine)
│
├── localhost (127.0.0.1)
│   └── LAB-01: Flask app on port 8080
│       └── SQLite DB: lab01.db (local file)
│
└── Host-only Network (192.168.56.0/24)
    └── LAB-02: VM at 192.168.56.20
        └── [Services NOT VERIFIED]
```

No direct network path exists between LAB-01 and LAB-02. They are isolated by design.