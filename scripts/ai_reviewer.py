import os
import subprocess
from openai import OpenAI


def get_diff(base_branch: str = "origin/main") -> str:
    try:
        diff = subprocess.check_output(
            ["git", "diff", base_branch, "HEAD"],
            stderr=subprocess.STDOUT,
        ).decode("utf-8")
        return diff
    except subprocess.CalledProcessError as e:
        print("Error getting git diff:", e.output.decode("utf-8"))
        return ""


def build_prompt(diff: str) -> str:
    instructions = """
You are a senior DevSecOps engineer and code reviewer.

Review the following code diff for:
- Security vulnerabilities (e.g., injection, insecure configs, secrets).
- Code quality issues (readability, error handling, duplication).
- DevSecOps best practices (logging, validation, least privilege).

For each issue:
- Quote the relevant code.
- Explain why it is a problem.
- Suggest a concrete fix.

If there are no changes, say that.
Code diff:
"""
    return instructions + "\n" + diff


def call_ai_model(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a strict but helpful code reviewer."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.2,
    )
    return response.choices[0].message.content


def main():
    diff = get_diff()
    if not diff.strip():
        print("No code changes detected. Nothing to review.")
        return

    prompt = build_prompt(diff)
    review = call_ai_model(prompt)

    print("==== AI CODE REVIEW START ====")
    print(review)
    print("==== AI CODE REVIEW END ====")


if __name__ == "__main__":
    main()
