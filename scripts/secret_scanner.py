import re


# Patterns for actual secrets
PATTERNS = {
    "OpenAI API Key": r"sk-[A-Za-z0-9]{20,}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "JWT Token": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "Private Key": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "Password": r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{8,}['\"]",
    "API Key": r"(?i)(api[_-]?key|apikey)\s*=\s*['\"][^'\"]{8,}['\"]",
    "Secret Key": r"(?i)(secret[_-]?key|secretkey)\s*=\s*['\"][^'\"]{8,}['\"]",
}


# Words that usually indicate documentation/examples
IGNORE_WORDS = [
    "example",
    "sample",
    "dummy",
    "test",
    "testing",
    "placeholder",
    "your_key",
    "your-secret",
    "xxxx",
    "changeme",
    "replace_me",
]


# Files that should not trigger secret detection
IGNORE_FILES = [
    ".md",
    ".txt",
    ".rst",
]


def should_ignore_line(line):
    """
    Ignore documentation, comments and fake examples.
    """

    lower = line.lower()

    # Ignore comments
    if line.strip().startswith("#"):
        return True

    # Ignore obvious examples/placeholders
    for word in IGNORE_WORDS:
        if word in lower:
            return True

    return False


def scan_for_secrets(code: str):

    issues = []

    for line_number, line in enumerate(code.splitlines(), start=1):

        # Only scan added git diff lines
        if not line.startswith("+") or line.startswith("+++"):
            continue


        clean_line = line[1:].strip()


        # Ignore comments and examples
        if should_ignore_line(clean_line):
            continue


        for name, pattern in PATTERNS.items():

            if re.search(pattern, clean_line):

                issues.append(
                    {
                        "type": name,
                        "severity": "HIGH",
                        "line": line_number,
                        "code": clean_line
                    }
                )


    return issues