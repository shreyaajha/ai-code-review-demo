import re


PATTERNS = {
    "OpenAI API Key": r"sk-[A-Za-z0-9]{20,}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "JWT Token": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "Private Key": r"-----BEGIN PRIVATE KEY-----",
    "Password": r"(?i)password\s*=\s*['\"].+?['\"]",
    "API Key": r"(?i)api[_-]?key\s*=\s*['\"].+?['\"]",
    "Secret Key": r"(?i)secret[_-]?key\s*=\s*['\"].+?['\"]",
}


def scan_for_secrets(code: str):
    issues = []

    for line_number, line in enumerate(code.splitlines(), start=1):

        if not line.startswith("+") or line.startswith("+++"):
            continue

        for name, pattern in PATTERNS.items():

            if re.search(pattern, line):

                issues.append({
                    "type": name,
                    "severity": "HIGH",
                    "line": line_number,
                    "code": line.strip()
                })

    return issues