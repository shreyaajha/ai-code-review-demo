from datetime import datetime
import uuid

from fastapi import FastAPI

from app.models import (
    Finding,
    ReviewRequest,
    ReviewResponse,
    Summary,
)

from scripts.secret_scanner import scan_for_secrets
from scripts.quality_checker import check_code_quality
from scripts.ai_reviewer import ai_review

app = FastAPI(
    title="AI DevSecOps Review API",
    version="3.0.0",
    description="Enterprise AI Code Review Service",
)


@app.get("/")
def home():
    return {
        "service": "AI DevSecOps Review API",
        "version": "3.0.0",
        "status": "Running"
    }


def calculate_summary(secret_results, quality_results, ai_result):

    critical = 0
    high = 0
    medium = 0
    low = 0

    score = 100

    recommendations = []

    for issue in secret_results:

        severity = issue["severity"].lower()

        if severity == "critical":
            critical += 1
            score -= 40

        elif severity == "high":
            high += 1
            score -= 20

        elif severity == "medium":
            medium += 1
            score -= 10

        else:
            low += 1
            score -= 5

        recommendations.append(
            f"Remove {issue['type']} from source code."
        )

    for issue in quality_results:

        severity = issue["severity"].lower()

        if severity == "critical":
            critical += 1
            score -= 40

        elif severity == "high":
            high += 1
            score -= 20

        elif severity == "medium":
            medium += 1
            score -= 10

        else:
            low += 1
            score -= 5

        recommendations.append(issue["message"])

    ai_upper = ai_result.upper()

    confidence = 95

    if "CRITICAL" in ai_upper:
        critical += 1

    elif "HIGH" in ai_upper:
        high += 1

    elif "MEDIUM" in ai_upper:
        medium += 1

    elif "LOW" in ai_upper:
        low += 1

    if score < 0:
        score = 0

    if critical:
        risk = "CRITICAL"

    elif high:
        risk = "HIGH"

    elif medium:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    return (
        Summary(
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            risk=risk,
            security_score=score,
            ai_confidence=confidence,
        ),
        recommendations,
    )


@app.post("/review", response_model=ReviewResponse)
def review(request: ReviewRequest):

    diff = request.diff

    secret_results = scan_for_secrets(diff)

    quality_results = check_code_quality(diff)

    ai_result = ai_review(diff)

    summary, recommendations = calculate_summary(
        secret_results,
        quality_results,
        ai_result,
    )

    findings = []

    for issue in secret_results:

        findings.append(
            Finding(
                type=issue["type"],
                line=issue["line"],
                code=issue["code"],
                severity=issue["severity"],
            )
        )

    status = "PASS"

    if (
        summary.critical
        or summary.high
        or ai_result.strip().startswith("FAIL")
    ):
        status = "FAIL"

    return ReviewResponse(

        review_id=str(uuid.uuid4())[:8],

        repository=request.repository,

        branch=request.branch,

        reviewed_at=datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        ),

        status=status,

        summary=summary,

        recommendations=recommendations,

        secret_scan=findings,

        quality_scan=quality_results,

        ai_review=ai_result,
    )