import os
import subprocess

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_diff(base_branch: str = "origin/main") -> str:
    """
    Returns the git diff between the current branch and the base branch.
    """
    try:
        diff = subprocess.check_output(
            ["git", "diff", base_branch, "HEAD"],
            stderr=subprocess.STDOUT,
        ).decode("utf-8")

        return diff

    except subprocess.CalledProcessError as e:
        print("Error getting git diff:")
        print(e.output.decode("utf-8"))
        return ""


def build_prompt(diff: str) -> str:
    """
    Builds the prompt sent to the AI.
    """

    instructions = """
You are a Senior DevSecOps Engineer and Expert Code Reviewer.

Review ONLY the provided Git diff.

Focus on:

- Security vulnerabilities
- Hardcoded secrets
- Logic bugs
- Performance issues
- Poor coding practices
- Missing exception handling
- Input validation
- Maintainability

Ignore:
- Formatting issues
- Minor style differences
- Missing comments unless they affect understanding

------------------------------------------

Return your response EXACTLY in this format.

# Result

PASS

No major issues found.

OR

# Result

FAIL

## Issue 1

Severity:
HIGH / MEDIUM / LOW

Problem:

Why it matters:

Suggested Fix:

## Issue 2

Severity:

Problem:

Why it matters:

Suggested Fix:

------------------------------------------

Git Diff:

"""

    return instructions + diff


def call_ai_model(prompt: str) -> str:
    """
    Sends the prompt to OpenRouter.
    """

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "FAIL\nOPENROUTER_API_KEY not found."

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    try:

        response = client.chat.completions.create(

            # Free Router (automatically picks an available free model)
            model="cohere/north-mini-code:free",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict but helpful Senior DevSecOps "
                        "Engineer and Code Reviewer."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.2,
            max_tokens=1500,

            extra_headers={
                "HTTP-Referer": "https://github.com/shreyaajha/ai-code-review-demo",
                "X-Title": "AI Code Reviewer",
            },
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"FAIL\n\nAI Review Error:\n{e}"


def ai_review(diff: str) -> str:
    """
    Performs AI review.
    """

    if not diff.strip():
        return "PASS\nNo code changes detected."

    prompt = build_prompt(diff)

    return call_ai_model(prompt)


def main():
    diff = get_diff()

    if not diff.strip():
        print("No code changes detected.")
        return

    print("\n==============================")
    print("🤖 AI REVIEW")
    print("==============================\n")

    review = ai_review(diff)

    print(review)


if __name__ == "__main__":
    main()