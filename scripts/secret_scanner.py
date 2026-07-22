import re
import os


PATTERNS = {
    "OpenAI API Key": r"sk-[A-Za-z0-9]{20,}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "JWT Token": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "Private Key": r"-----BEGIN PRIVATE KEY-----",
    "Password": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{8,}['\"]",
    "API Key": r"(?i)(api[_-]?key|apikey)\s*=\s*['\"][^'\"]{8,}['\"]",
    "Secret Key": r"(?i)(secret[_-]?key|secretkey)\s*=\s*['\"][^'\"]{8,}['\"]",
}


IGNORE_FILES = [
    "README.md",
    "test_secret.py",
    "test_app.py",
]


def scan_for_secrets(code: str):

    issues = []

    current_file = ""

    for line_number, line in enumerate(code.splitlines(), start=1):

        # detect filename from git diff
        if line.startswith("+++ b/"):
            current_file = line.replace("+++ b/", "").strip()

        # ignore documentation/tests
        if any(current_file.endswith(file) for file in IGNORE_FILES):
            continue


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