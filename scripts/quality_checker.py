def check_code_quality(code: str):

    issues = []

    lines = code.splitlines()

    for line_number, line in enumerate(lines, start=1):

        # Only check newly added lines
        if not line.startswith("+") or line.startswith("+++"):
            continue

        current = line.lower()

        # TODO comments
        if "todo" in current:
            issues.append({
                "type": "TODO Comment",
                "line": line_number,
                "severity": "Medium",
                "message": "Resolve TODO before merging."
            })

        # Debug statements
        if "console.log(" in current:
            issues.append({
                "type": "Debug Statement",
                "line": line_number,
                "severity": "Low",
                "message": "Remove console.log before pushing."
            })

        if "print(" in current:
            issues.append({
                "type": "Debug Statement",
                "line": line_number,
                "severity": "Low",
                "message": "Remove print() before pushing."
            })

        # Python debugger
        if "breakpoint(" in current:
            issues.append({
                "type": "Debugger",
                "line": line_number,
                "severity": "Medium",
                "message": "Remove breakpoint() before pushing."
            })

        # JavaScript debugger
        if "debugger;" in current:
            issues.append({
                "type": "Debugger",
                "line": line_number,
                "severity": "Medium",
                "message": "Remove debugger statement."
            })

    return issues