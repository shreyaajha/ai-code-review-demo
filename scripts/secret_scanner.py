import re
import os


def scan_for_secrets(file_path):

    ignored_files = [
        "demo",
        "test",
        "example",
        "sample"
    ]

    for item in ignored_files:
        if item in file_path.lower():
            return []

    patterns = {

        "OpenAI API Key":
            r"sk-[A-Za-z0-9]{20,}",

        "AWS Access Key":
            r"AKIA[0-9A-Z]{16}",

        "JWT Token":
            r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",

        "Private Key":
            r"-----BEGIN PRIVATE KEY-----",

        "Password":
            r"password\s*=\s*['\"].+?['\"]",

        "Secret Key":
            r"secret[_-]?key\s*=\s*['\"].+?['\"]"
    }


    issues = []

    try:
        with open(file_path, "r", errors="ignore") as file:
            content = file.read()

    except FileNotFoundError:
        return []


    for pattern_name, pattern in patterns.items():

        if re.search(pattern, content, re.IGNORECASE):

            issues.append({
                "type": "Security",
                "issue": pattern_name,
                "file": file_path
            })


    return issues