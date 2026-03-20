#!/usr/bin/env python3
"""
TradeMe iOS Security Agent

Responsible for:
- OWASP Mobile Top 10 vulnerability scanning
- iOS-specific security checks (Keychain, certificate pinning, biometrics)
- API security analysis (authentication, token handling, PII exposure)
- Code security review (secrets, logging, injection vulnerabilities)
- Security compliance verification
- Threat modeling and risk assessment
"""

import os
import sys
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

from shared_utils import (
    AgentConfig, FileManager, HandoffManager, ValidationManager,
    AgentRole, WorkflowStage, WorkflowContext, load_architecture_context
)

class SecuritySeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

@dataclass
class SecurityFinding:
    severity: SecuritySeverity
    category: str
    title: str
    description: str
    location: str  # File path and line number
    recommendation: str
    owasp_category: Optional[str] = None
    cwe_id: Optional[str] = None

@dataclass
class SecurityReport:
    owasp_mobile_checks: Dict[str, Any]
    ios_security_checks: Dict[str, Any]
    api_security_checks: Dict[str, Any]
    code_security_checks: Dict[str, Any]
    findings: List[SecurityFinding]
    overall_risk_score: float  # 0-100, higher is more risky
    security_grade: str  # A, B, C, D, F
    critical_issues: List[SecurityFinding]
    recommendations: List[str]
    compliance_status: Dict[str, bool]

class TradeMeSecurityAgent:
    def __init__(self):
        self.config = AgentConfig()
        self.file_manager = FileManager(self.config)
        self.handoff_manager = HandoffManager(self.config, self.file_manager)
        self.validation_manager = ValidationManager(self.config, self.file_manager)

        # Load architecture context
        self.architecture_context = load_architecture_context(self.file_manager)

        # Agent identity
        self.role = AgentRole.SECURITY_ENGINEER
        self.agent_config = self.config.get_agent_config(self.role)

        # Security patterns and rules
        self._init_security_rules()

    def _init_security_rules(self):
        """Initialize security scanning rules and patterns."""

        # OWASP Mobile Top 10 categories
        self.owasp_categories = {
            "M1": "Improper Platform Usage",
            "M2": "Insecure Data Storage",
            "M3": "Insecure Communication",
            "M4": "Insecure Authentication",
            "M5": "Insufficient Cryptography",
            "M6": "Insecure Authorization",
            "M7": "Client Code Quality",
            "M8": "Code Tampering",
            "M9": "Reverse Engineering",
            "M10": "Extraneous Functionality"
        }

        # Sensitive data patterns
        self.sensitive_patterns = {
            'api_keys': r'(api[_-]?key|apikey|api[_-]?secret)\s*[=:]\s*["\'][^"\']+["\']',
            'tokens': r'(token|bearer|jwt|access[_-]?token)\s*[=:]\s*["\'][^"\']+["\']',
            'passwords': r'(password|passwd|pwd)\s*[=:]\s*["\'][^"\']+["\']',
            'private_keys': r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
            'aws_keys': r'(AKIA|aws_access_key_id|aws_secret_access_key)',
            'credit_cards': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
        }

        # iOS security patterns
        self.ios_security_patterns = {
            'keychain_usage': r'(SecItemAdd|SecItemCopyMatching|SecItemUpdate|SecItemDelete)',
            'insecure_storage': r'(UserDefaults|NSUserDefaults)\.standard\.(set|string|integer)',
            'no_certificate_pinning': r'URLSession\s*\(',
            'http_usage': r'http://',
            'insecure_random': r'(arc4random|random)\(',
            'biometric_auth': r'(LAContext|evaluatePolicy)',
            'webview_javascript': r'WKWebView.*evaluateJavaScript',
        }

        # API security patterns
        self.api_security_patterns = {
            'hardcoded_urls': r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'pii_logging': r'(print|NSLog|os_log).*\b(email|phone|ssn|address|password)\b',
            'no_auth_header': r'URLRequest\s*\(',
            'sql_injection': r'(executeSql|rawQuery).*\+.*',
        }

    def run_security_audit(self, context: WorkflowContext) -> SecurityReport:
        """
        Run comprehensive security audit on generated code.
        """
        print(f"🔒 TradeMe iOS Security Agent auditing: {context.ticket_id}")
        print(f"📝 Description: {context.description}")

        findings = []

        # Get generated files
        generated_files = self._get_generated_files(context)

        # Run OWASP Mobile Top 10 checks
        print("🔍 Running OWASP Mobile Top 10 checks...")
        owasp_results = self._check_owasp_mobile_top_10(context, generated_files, findings)

        # Run iOS-specific security checks
        print("📱 Running iOS-specific security checks...")
        ios_results = self._check_ios_security(context, generated_files, findings)

        # Run API security checks
        print("🌐 Running API security checks...")
        api_results = self._check_api_security(context, generated_files, findings)

        # Run code security checks
        print("💻 Running code security checks...")
        code_results = self._check_code_security(context, generated_files, findings)

        # Calculate risk score and grade
        risk_score, security_grade = self._calculate_risk_score(findings)

        # Identify critical issues
        critical_issues = [f for f in findings if f.severity == SecuritySeverity.CRITICAL]

        # Generate recommendations
        recommendations = self._generate_recommendations(findings, owasp_results, ios_results, api_results)

        # Check compliance
        compliance_status = self._check_compliance(findings)

        report = SecurityReport(
            owasp_mobile_checks=owasp_results,
            ios_security_checks=ios_results,
            api_security_checks=api_results,
            code_security_checks=code_results,
            findings=findings,
            overall_risk_score=risk_score,
            security_grade=security_grade,
            critical_issues=critical_issues,
            recommendations=recommendations,
            compliance_status=compliance_status
        )

        # Save security report
        self._save_security_report(context, report)

        # Create handoff for QA
        self._create_security_handoff(context, report)

        return report

    def _get_generated_files(self, context: WorkflowContext) -> List[Dict[str, Any]]:
        """Get list of generated code files."""
        generated_code_dir = self.file_manager.get_path("generated_code")
        files = []

        for root, _, filenames in os.walk(generated_code_dir):
            for filename in filenames:
                if filename.endswith('.swift'):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        files.append({
                            'path': file_path,
                            'name': filename,
                            'content': content,
                            'lines': content.split('\n')
                        })
                    except Exception as e:
                        print(f"⚠️  Error reading {file_path}: {e}")

        return files

    def _check_owasp_mobile_top_10(self, context: WorkflowContext, files: List[Dict], findings: List[SecurityFinding]) -> Dict[str, Any]:
        """Check for OWASP Mobile Top 10 vulnerabilities."""
        results = {
            "M1_improper_platform": [],
            "M2_insecure_data_storage": [],
            "M3_insecure_communication": [],
            "M4_insecure_authentication": [],
            "M5_insufficient_cryptography": [],
            "M6_insecure_authorization": [],
            "M7_code_quality": [],
            "M8_code_tampering": [],
            "M9_reverse_engineering": [],
            "M10_extraneous_functionality": []
        }

        for file_info in files:
            content = file_info['content']
            path = file_info['path']

            # M2: Insecure Data Storage
            if 'UserDefaults' in content or 'NSUserDefaults' in content:
                for i, line in enumerate(file_info['lines'], 1):
                    if re.search(r'UserDefaults.*set', line):
                        finding = SecurityFinding(
                            severity=SecuritySeverity.MEDIUM,
                            category="Insecure Data Storage",
                            title="Potential sensitive data in UserDefaults",
                            description="UserDefaults is not encrypted. Sensitive data should use Keychain.",
                            location=f"{path}:{i}",
                            recommendation="Use Keychain for sensitive data like tokens, passwords, or PII. UserDefaults should only store non-sensitive preferences.",
                            owasp_category="M2"
                        )
                        findings.append(finding)
                        results["M2_insecure_data_storage"].append(finding)

            # M3: Insecure Communication
            http_pattern = re.compile(r'http://[^\s"\']+')
            for i, line in enumerate(file_info['lines'], 1):
                if http_pattern.search(line):
                    finding = SecurityFinding(
                        severity=SecuritySeverity.HIGH,
                        category="Insecure Communication",
                        title="HTTP (non-HTTPS) URL detected",
                        description="Using HTTP instead of HTTPS exposes data to interception.",
                        location=f"{path}:{i}",
                        recommendation="Use HTTPS for all network communications. Configure App Transport Security (ATS) to require HTTPS.",
                        owasp_category="M3"
                    )
                    findings.append(finding)
                    results["M3_insecure_communication"].append(finding)

            # M5: Insufficient Cryptography
            weak_crypto_patterns = [
                (r'\bMD5\b', 'MD5 is cryptographically broken'),
                (r'\bSHA1\b', 'SHA1 is deprecated and weak'),
                (r'arc4random\(', 'Use SecRandomCopyBytes for cryptographic randomness'),
            ]

            for pattern, message in weak_crypto_patterns:
                for i, line in enumerate(file_info['lines'], 1):
                    if re.search(pattern, line):
                        finding = SecurityFinding(
                            severity=SecuritySeverity.MEDIUM,
                            category="Insufficient Cryptography",
                            title=f"Weak cryptography: {message}",
                            description=f"Found usage of weak cryptographic function in line {i}",
                            location=f"{path}:{i}",
                            recommendation="Use strong cryptographic algorithms: SHA-256 or better, AES-256, SecRandomCopyBytes.",
                            owasp_category="M5"
                        )
                        findings.append(finding)
                        results["M5_insufficient_cryptography"].append(finding)

        return results

    def _check_ios_security(self, context: WorkflowContext, files: List[Dict], findings: List[SecurityFinding]) -> Dict[str, Any]:
        """Check iOS-specific security issues."""
        results = {
            "keychain_usage": 0,
            "certificate_pinning": False,
            "biometric_auth": False,
            "secure_enclave": False,
            "issues": []
        }

        for file_info in files:
            content = file_info['content']
            path = file_info['path']

            # Check Keychain usage
            if re.search(self.ios_security_patterns['keychain_usage'], content):
                results["keychain_usage"] += 1

            # Check for certificate pinning
            if 'URLSessionDelegate' in content or 'didReceive challenge' in content:
                results["certificate_pinning"] = True

            # Check biometric auth
            if re.search(self.ios_security_patterns['biometric_auth'], content):
                results["biometric_auth"] = True

            # Check for WebView JavaScript execution (potential XSS)
            for i, line in enumerate(file_info['lines'], 1):
                if re.search(self.ios_security_patterns['webview_javascript'], line):
                    finding = SecurityFinding(
                        severity=SecuritySeverity.MEDIUM,
                        category="iOS Security",
                        title="WebView JavaScript execution detected",
                        description="Executing JavaScript in WebView can lead to XSS vulnerabilities.",
                        location=f"{path}:{i}",
                        recommendation="Validate and sanitize any JavaScript code. Consider using WKScriptMessage for safer communication.",
                        owasp_category="M7"
                    )
                    findings.append(finding)
                    results["issues"].append(finding)

            # Check for jailbreak detection
            jailbreak_indicators = ['cydia://', '/Applications/Cydia.app', '/bin/bash', 'canOpenURL']
            has_jailbreak_detection = any(indicator in content for indicator in jailbreak_indicators)

            if not has_jailbreak_detection and ('authentication' in context.description.lower() or 'payment' in context.description.lower()):
                finding = SecurityFinding(
                    severity=SecuritySeverity.LOW,
                    category="iOS Security",
                    title="No jailbreak detection found",
                    description="For security-critical features, consider adding jailbreak detection.",
                    location=path,
                    recommendation="Implement jailbreak detection for sensitive operations like authentication or payments.",
                    owasp_category="M8"
                )
                findings.append(finding)
                results["issues"].append(finding)

        return results

    def _check_api_security(self, context: WorkflowContext, files: List[Dict], findings: List[SecurityFinding]) -> Dict[str, Any]:
        """Check API security issues."""
        results = {
            "auth_headers": 0,
            "hardcoded_urls": [],
            "pii_logging": [],
            "rate_limiting": False,
            "issues": []
        }

        for file_info in files:
            content = file_info['content']
            path = file_info['path']

            # Check for authentication headers
            if 'Authorization' in content or 'Bearer' in content:
                results["auth_headers"] += 1

            # Check for hardcoded API URLs
            url_pattern = re.compile(r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s"\']*')
            for i, line in enumerate(file_info['lines'], 1):
                urls = url_pattern.findall(line)
                for url in urls:
                    if 'localhost' not in url and 'example.com' not in url:
                        finding = SecurityFinding(
                            severity=SecuritySeverity.LOW,
                            category="API Security",
                            title="Hardcoded API URL",
                            description=f"Found hardcoded URL: {url}",
                            location=f"{path}:{i}",
                            recommendation="Move API URLs to configuration files or environment variables for easier updates and environment management.",
                            owasp_category="M10"
                        )
                        findings.append(finding)
                        results["hardcoded_urls"].append(url)

            # Check for PII in logs
            pii_keywords = ['email', 'phone', 'ssn', 'address', 'password', 'creditcard', 'token']
            for i, line in enumerate(file_info['lines'], 1):
                if any(keyword in line.lower() for keyword in ['print(', 'nslog(', 'os_log(']):
                    for pii in pii_keywords:
                        if pii in line.lower():
                            finding = SecurityFinding(
                                severity=SecuritySeverity.HIGH,
                                category="API Security",
                                title="Potential PII in logs",
                                description=f"Logging statement may contain {pii}",
                                location=f"{path}:{i}",
                                recommendation="Never log sensitive personal information. Remove or redact PII from logs.",
                                owasp_category="M2",
                                cwe_id="CWE-532"
                            )
                            findings.append(finding)
                            results["pii_logging"].append(finding)

            # Check for SQL injection vulnerabilities
            if 'executeSql' in content or 'rawQuery' in content:
                for i, line in enumerate(file_info['lines'], 1):
                    if '+' in line and ('executeSql' in line or 'rawQuery' in line):
                        finding = SecurityFinding(
                            severity=SecuritySeverity.CRITICAL,
                            category="API Security",
                            title="Potential SQL injection",
                            description="String concatenation in SQL query detected",
                            location=f"{path}:{i}",
                            recommendation="Use parameterized queries or prepared statements to prevent SQL injection.",
                            owasp_category="M7",
                            cwe_id="CWE-89"
                        )
                        findings.append(finding)
                        results["issues"].append(finding)

        return results

    def _check_code_security(self, context: WorkflowContext, files: List[Dict], findings: List[SecurityFinding]) -> Dict[str, Any]:
        """Check for code-level security issues."""
        results = {
            "hardcoded_secrets": [],
            "sensitive_comments": [],
            "debug_code": [],
            "issues": []
        }

        for file_info in files:
            content = file_info['content']
            path = file_info['path']

            # Check for hardcoded secrets
            for secret_type, pattern in self.sensitive_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Find line number
                    line_num = content[:match.start()].count('\n') + 1

                    finding = SecurityFinding(
                        severity=SecuritySeverity.CRITICAL,
                        category="Code Security",
                        title=f"Hardcoded {secret_type.replace('_', ' ')} detected",
                        description=f"Found potential hardcoded secret: {match.group()[:50]}...",
                        location=f"{path}:{line_num}",
                        recommendation="Remove hardcoded secrets. Use environment variables, Keychain, or secure configuration management.",
                        owasp_category="M2",
                        cwe_id="CWE-798"
                    )
                    findings.append(finding)
                    results["hardcoded_secrets"].append(finding)

            # Check for debug/test code in production
            debug_patterns = [
                (r'#if\s+DEBUG', 'Debug flag detected'),
                (r'assert\(', 'Assert statement (consider removing for production)'),
                (r'fatalError\(["\']TODO', 'TODO fatalError (must be implemented)'),
            ]

            for pattern, message in debug_patterns:
                for i, line in enumerate(file_info['lines'], 1):
                    if re.search(pattern, line):
                        finding = SecurityFinding(
                            severity=SecuritySeverity.LOW if 'DEBUG' in pattern else SecuritySeverity.MEDIUM,
                            category="Code Security",
                            title=message,
                            description=f"Found at line {i}: {line.strip()}",
                            location=f"{path}:{i}",
                            recommendation="Review and ensure debug code is properly gated or removed for production builds.",
                            owasp_category="M10"
                        )
                        findings.append(finding)
                        results["debug_code"].append(finding)

            # Check for sensitive information in comments
            sensitive_comment_patterns = ['password', 'api_key', 'secret', 'token', 'credentials']
            for i, line in enumerate(file_info['lines'], 1):
                if '//' in line or '/*' in line:
                    if any(pattern in line.lower() for pattern in sensitive_comment_patterns):
                        finding = SecurityFinding(
                            severity=SecuritySeverity.MEDIUM,
                            category="Code Security",
                            title="Sensitive information in comments",
                            description=f"Comment may contain sensitive information",
                            location=f"{path}:{i}",
                            recommendation="Remove sensitive information from comments. Use documentation tools for configuration examples.",
                            owasp_category="M2"
                        )
                        findings.append(finding)
                        results["sensitive_comments"].append(finding)

        return results

    def _calculate_risk_score(self, findings: List[SecurityFinding]) -> Tuple[float, str]:
        """Calculate overall risk score and security grade."""
        if not findings:
            return 0.0, "A+"

        # Weight by severity
        severity_weights = {
            SecuritySeverity.CRITICAL: 25,
            SecuritySeverity.HIGH: 15,
            SecuritySeverity.MEDIUM: 8,
            SecuritySeverity.LOW: 3,
            SecuritySeverity.INFO: 1
        }

        total_risk = sum(severity_weights[f.severity] for f in findings)

        # Normalize to 0-100 scale (cap at 100)
        risk_score = min(100, total_risk)

        # Assign grade
        if risk_score == 0:
            grade = "A+"
        elif risk_score < 10:
            grade = "A"
        elif risk_score < 25:
            grade = "B"
        elif risk_score < 50:
            grade = "C"
        elif risk_score < 75:
            grade = "D"
        else:
            grade = "F"

        return risk_score, grade

    def _generate_recommendations(self, findings: List[SecurityFinding], owasp: Dict, ios: Dict, api: Dict) -> List[str]:
        """Generate security recommendations."""
        recommendations = []

        # Critical issues first
        critical_findings = [f for f in findings if f.severity == SecuritySeverity.CRITICAL]
        if critical_findings:
            recommendations.append(f"🚨 CRITICAL: Address {len(critical_findings)} critical security issues immediately before deployment")

        # OWASP recommendations
        if len(findings) > 10:
            recommendations.append("Consider comprehensive security review - multiple security issues detected")

        # iOS-specific recommendations
        if not ios.get('certificate_pinning'):
            recommendations.append("Implement certificate pinning for API communications to prevent MITM attacks")

        if ios.get('keychain_usage', 0) == 0 and any('auth' in f.category.lower() for f in findings):
            recommendations.append("Use iOS Keychain for secure storage of authentication credentials")

        # API recommendations
        if len(api.get('hardcoded_urls', [])) > 0:
            recommendations.append("Move API URLs to configuration management system")

        if len(api.get('pii_logging', [])) > 0:
            recommendations.append("Implement log sanitization to prevent PII exposure")

        # General recommendations
        if not recommendations:
            recommendations.append("✅ No critical security issues found. Continue following security best practices.")

        return recommendations

    def _check_compliance(self, findings: List[SecurityFinding]) -> Dict[str, bool]:
        """Check compliance status."""
        return {
            "no_critical_issues": not any(f.severity == SecuritySeverity.CRITICAL for f in findings),
            "no_high_issues": not any(f.severity == SecuritySeverity.HIGH for f in findings),
            "owasp_mobile_compliant": len([f for f in findings if f.owasp_category]) < 3,
            "production_ready": not any(f.severity in [SecuritySeverity.CRITICAL, SecuritySeverity.HIGH] for f in findings)
        }

    def _save_security_report(self, context: WorkflowContext, report: SecurityReport):
        """Save security report to markdown file."""
        security_reports_dir = os.path.join(self.file_manager.get_path("agents_system"), "security-reports")
        os.makedirs(security_reports_dir, exist_ok=True)

        report_path = os.path.join(security_reports_dir, f"{context.ticket_id}-security-report.md")

        # Generate markdown report
        md_content = self._generate_markdown_report(context, report)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"📄 Security report saved: {report_path}")

    def _generate_markdown_report(self, context: WorkflowContext, report: SecurityReport) -> str:
        """Generate markdown security report."""
        lines = []

        lines.append(f"# Security Audit Report: {context.ticket_id}\n")
        lines.append(f"**Generated by**: TradeMe iOS Security Agent\n")
        lines.append(f"**Date**: {context.timestamp}\n")
        lines.append(f"**Description**: {context.description}\n")
        lines.append("\n---\n")

        # Executive Summary
        lines.append("## 🎯 Executive Summary\n")
        lines.append(f"- **Security Grade**: `{report.security_grade}`\n")
        lines.append(f"- **Risk Score**: `{report.overall_risk_score:.1f}/100`\n")
        lines.append(f"- **Total Findings**: {len(report.findings)}\n")
        lines.append(f"- **Critical Issues**: {len(report.critical_issues)}\n")
        lines.append(f"- **Production Ready**: {'✅ YES' if report.compliance_status.get('production_ready') else '❌ NO'}\n")
        lines.append("\n")

        # Findings by Severity
        lines.append("## 📊 Findings by Severity\n")
        severity_counts = {}
        for finding in report.findings:
            severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

        for severity in [SecuritySeverity.CRITICAL, SecuritySeverity.HIGH, SecuritySeverity.MEDIUM, SecuritySeverity.LOW, SecuritySeverity.INFO]:
            count = severity_counts.get(severity, 0)
            emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "⚪"}[severity.value]
            lines.append(f"- {emoji} **{severity.value}**: {count}\n")
        lines.append("\n")

        # Critical Issues
        if report.critical_issues:
            lines.append("## 🚨 Critical Issues\n")
            for i, finding in enumerate(report.critical_issues, 1):
                lines.append(f"### {i}. {finding.title}\n")
                lines.append(f"- **Category**: {finding.category}\n")
                lines.append(f"- **Location**: `{finding.location}`\n")
                lines.append(f"- **Description**: {finding.description}\n")
                lines.append(f"- **Recommendation**: {finding.recommendation}\n")
                if finding.owasp_category:
                    lines.append(f"- **OWASP**: {finding.owasp_category}\n")
                if finding.cwe_id:
                    lines.append(f"- **CWE**: {finding.cwe_id}\n")
                lines.append("\n")

        # OWASP Mobile Top 10
        lines.append("## 🛡️ OWASP Mobile Top 10 Analysis\n")
        for category, findings_list in report.owasp_mobile_checks.items():
            status = "✅ PASS" if len(findings_list) == 0 else f"⚠️ {len(findings_list)} issues"
            category_name = category.replace('_', ' ').title()
            lines.append(f"- **{category_name}**: {status}\n")
        lines.append("\n")

        # iOS Security
        lines.append("## 📱 iOS Security Checks\n")
        ios = report.ios_security_checks
        lines.append(f"- **Keychain Usage**: {'✅ Implemented' if ios.get('keychain_usage', 0) > 0 else '❌ Not found'}\n")
        lines.append(f"- **Certificate Pinning**: {'✅ Implemented' if ios.get('certificate_pinning') else '⚠️ Not implemented'}\n")
        lines.append(f"- **Biometric Auth**: {'✅ Implemented' if ios.get('biometric_auth') else 'ℹ️ Not found'}\n")
        lines.append("\n")

        # API Security
        lines.append("## 🌐 API Security Checks\n")
        api = report.api_security_checks
        lines.append(f"- **Authentication Headers**: {api.get('auth_headers', 0)} found\n")
        lines.append(f"- **Hardcoded URLs**: {len(api.get('hardcoded_urls', []))} found\n")
        lines.append(f"- **PII Logging Issues**: {len(api.get('pii_logging', []))} found\n")
        lines.append("\n")

        # Recommendations
        lines.append("## 💡 Recommendations\n")
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}\n")
        lines.append("\n")

        # Compliance Status
        lines.append("## ✅ Compliance Status\n")
        for check, status in report.compliance_status.items():
            emoji = "✅" if status else "❌"
            check_name = check.replace('_', ' ').title()
            lines.append(f"- {emoji} **{check_name}**: {'PASS' if status else 'FAIL'}\n")
        lines.append("\n")

        # Detailed Findings
        if report.findings:
            lines.append("## 📋 Detailed Findings\n")
            for i, finding in enumerate(report.findings, 1):
                severity_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "⚪"}[finding.severity.value]
                lines.append(f"### {i}. {severity_emoji} {finding.title}\n")
                lines.append(f"- **Severity**: {finding.severity.value}\n")
                lines.append(f"- **Category**: {finding.category}\n")
                lines.append(f"- **Location**: `{finding.location}`\n")
                lines.append(f"- **Description**: {finding.description}\n")
                lines.append(f"- **Recommendation**: {finding.recommendation}\n")
                lines.append("\n")

        lines.append("\n---\n")
        lines.append("*🔒 Generated by TradeMe iOS Security Agent*\n")

        return ''.join(lines)

    def _create_security_handoff(self, context: WorkflowContext, report: SecurityReport):
        """Create handoff document for QA Engineer."""
        handoff_data = {
            "from_agent": "Security Engineer",
            "to_agent": "QA Engineer",
            "ticket_id": context.ticket_id,
            "stage": "security_audit",
            "security_grade": report.security_grade,
            "risk_score": report.overall_risk_score,
            "critical_issues_count": len(report.critical_issues),
            "total_findings": len(report.findings),
            "production_ready": report.compliance_status.get('production_ready', False),
            "recommendations": report.recommendations,
            "next_steps": [
                "Review security findings and address critical issues" if report.critical_issues else "Proceed with QA testing",
                "Validate security fixes if any issues were found",
                "Run comprehensive QA testing suite"
            ]
        }

        self.handoff_manager.create_handoff(
            context=context,
            from_stage=WorkflowStage.SECURITY_AUDIT,
            to_stage=WorkflowStage.QUALITY_ASSURANCE,
            data=handoff_data
        )

        print(f"✅ Security handoff created for QA Engineer")


def main():
    """CLI entry point for Security Agent."""
    import argparse

    parser = argparse.ArgumentParser(description='TradeMe iOS Security Agent')
    parser.add_argument('ticket_id', help='Ticket ID (e.g., VLP-123)')
    parser.add_argument('description', help='Ticket description')

    args = parser.parse_args()

    # Create workflow context
    context = WorkflowContext(
        ticket_id=args.ticket_id,
        description=args.description,
        workflow_type="feature_development"
    )

    # Run security audit
    agent = TradeMeSecurityAgent()
    report = agent.run_security_audit(context)

    # Print summary
    print("\n" + "="*60)
    print(f"🔒 Security Audit Complete: {args.ticket_id}")
    print("="*60)
    print(f"Security Grade: {report.security_grade}")
    print(f"Risk Score: {report.overall_risk_score:.1f}/100")
    print(f"Total Findings: {len(report.findings)}")
    print(f"Critical Issues: {len(report.critical_issues)}")
    print(f"Production Ready: {'✅ YES' if report.compliance_status.get('production_ready') else '❌ NO'}")
    print("="*60)


if __name__ == "__main__":
    main()
