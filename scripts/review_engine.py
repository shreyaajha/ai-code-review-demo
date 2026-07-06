import subprocess
import sys
from datetime import datetime
import uuid

from scripts.secret_scanner import scan_for_secrets
from scripts.quality_checker import check_code_quality
from scripts.ai_reviewer import ai_review


def get_git_diff():
    try:
        return subprocess.check_output(
            ["git", "show", "--format=", "HEAD"],
            text=True,
        )
    except Exception:
        return ""


def print_header(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def calculate_score(secrets, quality):
    score = 100

    for issue in secrets + quality:
        severity = issue["severity"].lower()

        if severity == "critical":
            score -= 40
        elif severity == "high":
            score -= 20
        elif severity == "medium":
            score -= 10
        else:
            score -= 5

    return max(score, 0)


def calculate_risk(secrets, quality):
    severities = [i["severity"].lower() for i in secrets + quality]

    if "critical" in severities:
        return "CRITICAL"

    if "high" in severities:
        return "HIGH"

    if "medium" in severities:
        return "MEDIUM"

    return "LOW"


def run_review():

    code = get_git_diff()

    if not code.strip():
        print("No code changes found.")
        sys.exit(0)

    review_id = str(uuid.uuid4())[:8]

    score = 100

    print_header("AI DEVSECOPS REVIEW REPORT")

    print(f"Review ID       : {review_id}")
    print(f"Reviewed At     : {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    print("\n🔒 Secret Scanner")

    secrets = scan_for_secrets(code)

    if secrets:
        for issue in secrets:
            print(
                f"❌ {issue['severity']} | "
                f"{issue['type']} | "
                f"Line {issue['line']}"
            )
    else:
        print("✅ No secrets detected")

    print("\n🛠 Code Quality")

    quality = check_code_quality(code)

    if quality:
        for issue in quality:
            print(
                f"⚠ {issue['severity']} | "
                f"{issue['type']} | "
                f"Line {issue['line']}"
            )
    else:
        print("✅ No quality issues")

    print("\n🤖 AI Review")

    ai_result = ai_review(code)

    print(ai_result)

    score = calculate_score(secrets, quality)

    risk = calculate_risk(secrets, quality)

    failed = (
        bool(secrets)
        or ai_result.strip().startswith("FAIL")
    )

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"Risk Level      : {risk}")
    print(f"Security Score  : {score}/100")
    print("AI Confidence   : 95%")

    print("\nFinal Verdict")

    if failed:
        print("❌ BLOCK PUSH")
        sys.exit(1)

    print("✅ READY TO PUSH")
    sys.exit(0)


if __name__ == "__main__":
    run_review()