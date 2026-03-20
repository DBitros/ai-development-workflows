---
description: Run security scan on generated code
---

# Security Scan

Quick security audit on generated code without full workflow.

## Usage

```bash
# Scan specific ticket
/security-scan VLP-123

# Scan latest generated code
/security-scan
```

## What It Does

Runs the Security Engineer Agent independently to:

1. **OWASP Mobile Top 10 Scan**
   - M1: Improper Platform Usage
   - M2: Insecure Data Storage
   - M3: Insecure Communication
   - M4: Insecure Authentication
   - M5: Insufficient Cryptography
   - M6: Insecure Authorization
   - M7: Client Code Quality
   - M8: Code Tampering
   - M9: Reverse Engineering
   - M10: Extraneous Functionality

2. **iOS-Specific Security**
   - Keychain usage validation
   - Certificate pinning check
   - Biometric authentication review
   - WebView security analysis

3. **API Security**
   - Authentication flow validation
   - Token handling review
   - PII exposure check
   - SQL injection scan

4. **Code Security**
   - Hardcoded secrets detection
   - Sensitive logging review
   - Debug code in production check

## Output

Security report with:
- Risk Score (0-100, lower is better)
- Security Grade (A+ to F)
- Detailed findings by severity
- Remediation recommendations
- Compliance status

**Report Location**: `security-reports/[TICKET-ID]-security-report.md`

## Example Output

```
🔒 Security Scan Complete: VLP-123

Security Grade: B
Risk Score: 15/100

Findings:
  🔴 CRITICAL: 0
  🟠 HIGH: 1
  🟡 MEDIUM: 3
  🔵 LOW: 2

Critical Issues to Address:
  (none)

High Priority Issues:
  1. Hardcoded API URL detected
     Location: UserProfileCache.swift:45
     Recommendation: Move to configuration

Production Ready: ⚠️ REVIEW REQUIRED

Full report: security-reports/VLP-123-security-report.md
```

## Execution

When invoked:

1. Read generated code from `generated-code/` directory
2. Run comprehensive security scans
3. Generate security report
4. Display summary to user
5. Highlight critical/high issues requiring immediate attention

## When to Use

- **After code generation** - Before committing code
- **Before PR creation** - Ensure no security issues
- **Quick security check** - Fast validation without full workflow
- **Security review** - Independent security audit

---

*🔒 Powered by TradeMe Security Engineer Agent*
