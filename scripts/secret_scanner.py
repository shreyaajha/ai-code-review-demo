import re

PATTERNS = {
    "OpenAI API Key": r"sk-[A-Za-z0-9_-]{20,}",

    "AWS Access Key": r"AKIA[0-9A-Z]{16}",

    "JWT Token": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",

    "Private Key": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",

    "GitHub Token": r"gh[pousr]_[A-Za-z0-9]{36,}",

    "Generic Secret":
        r"\b(password|passwd|pwd|secret|secret_key|client_secret|"
        r"access_token|refresh_token|auth_token|token|"
        r"api[_-]?key|api[_-]?keys|apikey|database_url|db_password)\b"
        r"\s*[:=]\s*[\"']?.+[\"']?"
}


HIGH_ENTROPY = re.compile(r"[A-Za-z0-9_\-]{24,}")


def looks_random(text: str) -> bool:
    """
    Simple heuristic:
    Long strings containing uppercase, lowercase and numbers
    are likely secrets.
    """

    if len(text) < 24:
        return False

    has_upper = any(c.isupper() for c in text)
    has_lower = any(c.islower() for c in text)
    has_digit = any(c.isdigit() for c in text)

    return has_upper and has_lower and has_digit


def scan_for_secrets(code: str):
    findings = []

    lines = code.splitlines()

    for line_number, line in enumerate(lines, start=1):

        # Scan only added lines in git diff
        if not line.startswith("+") or line.startswith("+++"):
            continue

        # Regex-based detection
        for secret_name, pattern in PATTERNS.items():

            if re.search(pattern, line, re.IGNORECASE):
                findings.append({
                    "type": secret_name,
                    "line": line_number,
                    "code": line.strip(),
                    "severity": "Critical"
                })

        # Detect suspicious random strings
        for candidate in HIGH_ENTROPY.findall(line):

            if looks_random(candidate):
                findings.append({
                    "type": "Possible Secret (High Entropy)",
                    "line": line_number,
                    "code": candidate,
                    "severity": "Medium"
                })

    return findings