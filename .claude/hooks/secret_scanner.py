#!/usr/bin/env python3
"""
PreToolUse hook for Write and Edit tool calls.

Scans the file content that is about to be written for common secret patterns:
  - Hardcoded passwords
  - Azure Storage account keys
  - Azure connection strings with embedded keys
  - AWS access key IDs
  - Bearer JWT tokens
  - Generic API keys
  - Private SSH/RSA keys
  - Azure subscription / tenant / client IDs in plaintext

If any pattern matches, the write is blocked with exit code 2 and the
location is reported (value is NEVER logged — only the type and location).
"""
import json
import sys
import re


SECRET_PATTERNS = [
    (
        r"(?:Password|Pwd|password|passwd)\s*=\s*['\"][^'\"]{4,}['\"]",
        "Hardcoded password",
    ),
    (
        r"(?:AccountKey|account_key)\s*=\s*['\"][A-Za-z0-9+/=]{50,}['\"]",
        "Azure Storage account key",
    ),
    (
        r"DefaultEndpointsProtocol=https.*AccountKey=[A-Za-z0-9+/=]{50,}",
        "Azure connection string with embedded key",
    ),
    (
        r"\bAKIA[0-9A-Z]{16}\b",
        "AWS access key ID",
    ),
    (
        r"Bearer\s+[A-Za-z0-9_\-=]+\.[A-Za-z0-9_\-=]+\.[A-Za-z0-9_\-=]+",
        "Bearer JWT token",
    ),
    (
        r"(?:api_key|apikey|api-key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]",
        "API key",
    ),
    (
        r"-----BEGIN (?:RSA )?PRIVATE KEY-----",
        "Private SSH/RSA key",
    ),
    (
        r"(?:subscriptionId|subscription_id)\s*[:=]\s*['\"][0-9a-f\-]{36}['\"]",
        "Azure subscription ID in plaintext",
    ),
    (
        r"(?:tenantId|tenant_id)\s*[:=]\s*['\"][0-9a-f\-]{36}['\"]",
        "Azure tenant ID in plaintext",
    ),
    (
        r"(?:clientId|client_id)\s*[:=]\s*['\"][0-9a-f\-]{36}['\"]",
        "Azure client ID in plaintext",
    ),
    (
        r"(?:clientSecret|client_secret)\s*[:=]\s*['\"][A-Za-z0-9_\-\.~]{20,}['\"]",
        "Azure client secret in plaintext",
    ),
]


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    content = data.get("tool_input", {}).get("content", "")
    file_path = data.get("tool_input", {}).get("file_path", "<unknown>")

    if not content:
        sys.exit(0)

    findings = []
    for pattern, description in SECRET_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            findings.append(f"{description} ({len(matches)} occurrence(s))")

    if findings:
        print(
            f"[SECRET_SCANNER BLOCKED] Potential secrets detected in: {file_path}",
            file=sys.stderr,
        )
        for finding in findings:
            print(f"  • {finding}", file=sys.stderr)
        print(
            "  → Use environment variables or Azure Key Vault references instead.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
