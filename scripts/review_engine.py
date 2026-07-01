import sys
import subprocess

from scripts.secret_scanner import scan_for_secrets
from scripts.quality_checker import check_code_quality
from scripts.ai_reviewer import ai_review


def get_git_diff():
    """
    Get the changes from the most recent commit.
    This is what is about to be pushed.
    """
    try:
        diff = subprocess.check_output(
            ["git", "show", "--format=", "HEAD"]
        ).decode("utf-8")

        return diff

    except Exception:
        return ""


def run_review():
    code = get_git_diff()

    if not code.strip():
        print("PASS")
        print("No staged changes found.")
        sys.exit(0)

    failed = False

    print("\n==============================")
    print("AI CODE REVIEW REPORT")
    print("==============================\n")

    # ---------------- Secret Scanner ----------------

    print("🔒 Running Secret Scanner...\n")

    secrets = scan_for_secrets(code)

    if secrets:
        failed = True
        print("FAIL")
        print("Critical Secrets Found\n")

        for issue in secrets:
            print(issue)

    else:
        print("PASS")
        print("No secrets found.\n")

    # ---------------- Quality Checker ----------------

    print("\n🛠 Running Quality Checker...\n")

    quality = check_code_quality(code)

    if quality:
        print("WARNING")
        print("Code Quality Suggestions\n")

        for issue in quality:
            print(issue)

    else:
        print("PASS")
        print("No quality issues found.\n")

    # ---------------- AI Review ----------------

    print("\n🤖 AI REVIEW\n")

    try:
        ai_result = ai_review(code)
        print(ai_result)

        if ai_result.strip().startswith("FAIL"):
            failed = True

    except Exception as e:
        failed = True
        print("FAIL")
        print(e)

    # ---------------- Final Result ----------------

    print("\n==============================")

    if failed:
        print("FINAL RESULT : FAIL")
        print("❌ Push Blocked")
        print("==============================")
        sys.exit(1)

    print("FINAL RESULT : PASS")
    print("✅ Ready to Push")
    print("==============================")
    sys.exit(0)


if __name__ == "__main__":
    run_review()