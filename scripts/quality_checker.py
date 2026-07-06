def check_code_quality(code: str):

    issues = []

    lines = code.splitlines()

    for line_number, line in enumerate(lines, start=1):

        if not line.startswith("+") or line.startswith("+++"):
            continue

        current = line.lower()

        checks = [
            (
                "todo",
                {
                    "type": "TODO Comment",
                    "severity": "Medium",
                    "message": "Resolve TODO before merging."
                },
            ),
            (
                "console.log(",
                {
                    "type": "Debug Statement",
                    "severity": "Low",
                    "message": "Remove console.log()."
                },
            ),
            (
                "print(",
                {
                    "type": "Debug Statement",
                    "severity": "Low",
                    "message": "Remove print()."
                },
            ),
            (
                "breakpoint(",
                {
                    "type": "Debugger",
                    "severity": "Medium",
                    "message": "Remove breakpoint()."
                },
            ),
            (
                "debugger;",
                {
                    "type": "Debugger",
                    "severity": "Medium",
                    "message": "Remove debugger statement."
                },
            ),
        ]

        for keyword, issue in checks:
            if keyword in current:
                issues.append({
                    **issue,
                    "line": line_number,
                    "code": line.strip(),
                })

    return issues