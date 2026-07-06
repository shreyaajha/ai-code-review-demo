import re

PATTERNS = {
    "OpenAI API Key": r"sk-[A-Za-z0-9_-]{20,}",

    "AWS Access Key": r"AKIA[0-9A-Z]{16}",

    "JWT Token": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",

    "Private Key": r"-----BEGIN PRIVATE KEY-----",

    "Password": r"\bpassword\b\s*=\s*[\"'].*?[\"']",

    "Secret Key": r"\bsecret_key\b\s*=\s*[\"'].*?[\"']",

    "API Key": r"\b(api[_-]?key|apikey|api[_-]?keys)\b\s*=\s*[\"'].*?[\"']",
}


def scan_for_secrets(code: str):
    findings = []

    lines = code.splitlines()

    for line_number, line in enumerate(lines, start=1):

        # Only scan added lines from the git diff
        if not line.startswith("+") or line.startswith("+++"):
            continue

        for secret_name, pattern in PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    "type": secret_name,
                    "line": line_number,
                    "code": line.strip(),
                    "severity": "Critical"
                })

    return findings