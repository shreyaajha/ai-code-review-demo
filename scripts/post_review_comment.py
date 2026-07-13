import json
import os
import requests

with open("review.json") as f:
    review = json.load(f)

comment = f"""
# 🤖 AI Code Review Report

**Status:** {review["status"]}

| Severity | Count |
|----------|--------|
| Critical | {review["summary"]["critical"]} |
| High | {review["summary"]["high"]} |
| Medium | {review["summary"]["medium"]} |
| Low | {review["summary"]["low"]} |
| Security Score | {review["summary"]["security_score"]}/100 |

## Recommendations

"""

for r in review["recommendations"]:
    comment += f"- {r}\n"

comment += "\n## AI Review\n"
comment += "```\n"
comment += review["ai_review"]
comment += "\n```"

repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
pr_number = os.environ["PR_NUMBER"]

url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

requests.post(
    url,
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    },
    json={"body": comment},
)