import json


def evaluate_compliance(
    response: str,
    output_format: str,
    role: str,
    safety_level: str,
) -> dict:
    """
    Perform deterministic compliance checks on an LLM response.
    """

    results = {}

    # --------------------------------------------------
    # JSON Format Check
    # --------------------------------------------------

    if output_format == "Strict JSON":

        try:
            data = json.loads(response)

            results["JSON Format"] = {
                "status": "PASS",
                "message": "Response is valid JSON.",
            }

        except json.JSONDecodeError:

            results["JSON Format"] = {
                "status": "FAIL",
                "message": "Response is not valid JSON.",
            }

            return results

    else:

        results["JSON Format"] = {
            "status": "N/A",
            "message": "JSON format was not required.",
        }

        data = None

    # --------------------------------------------------
    # Required Fields Check
    # --------------------------------------------------

    if output_format == "Strict JSON" and isinstance(data, dict):

        required_fields = {
            "summary",
            "analysis",
            "recommendation",
            "risks",
            "confidence",
        }

        actual_fields = set(data.keys())

        missing_fields = required_fields - actual_fields
        extra_fields = actual_fields - required_fields

        if not missing_fields and not extra_fields:

            results["Required Fields"] = {
                "status": "PASS",
                "message": "All required fields are present.",
            }

        else:

            messages = []

            if missing_fields:
                messages.append(
                    f"Missing: {', '.join(sorted(missing_fields))}"
                )

            if extra_fields:
                messages.append(
                    f"Unexpected: {', '.join(sorted(extra_fields))}"
                )

            results["Required Fields"] = {
                "status": "FAIL",
                "message": " | ".join(messages),
            }

    elif output_format == "Strict JSON":

        results["Required Fields"] = {
            "status": "FAIL",
            "message": "Expected a JSON object.",
        }

    else:

        results["Required Fields"] = {
            "status": "N/A",
            "message": "Structured fields were not required.",
        }

    # --------------------------------------------------
    # Role Check
    # --------------------------------------------------

    role_keywords = {
        "Senior AI Engineer": [
            "architecture",
            "system",
            "model",
            "deployment",
            "pipeline",
            "engineering",
        ],
        "Python Developer": [
            "python",
            "function",
            "class",
            "package",
            "code",
        ],
        "Data Scientist": [
            "data",
            "model",
            "feature",
            "dataset",
            "analysis",
        ],
        "Technical Research Assistant": [
            "research",
            "evidence",
            "method",
            "analysis",
            "findings",
        ],
    }

    response_lower = response.lower()

    keywords = role_keywords.get(role, [])

    matched_keywords = [
        keyword
        for keyword in keywords
        if keyword in response_lower
    ]

    if matched_keywords:

        results["Role Alignment"] = {
            "status": "PASS",
            "message": (
                f"Response contains role-relevant concepts: "
                f"{', '.join(matched_keywords[:3])}"
            ),
        }

    else:

        results["Role Alignment"] = {
            "status": "REVIEW",
            "message": "No strong role-specific keywords detected.",
        }

    # --------------------------------------------------
    # Safety Check
    # --------------------------------------------------

    if safety_level == "Strict":

        sensitive_patterns = [
            "api_key",
            "password",
            "secret",
            "private key",
            "access token",
        ]

        detected = [
            pattern
            for pattern in sensitive_patterns
            if pattern in response_lower
        ]

        if detected:

            results["Safety"] = {
                "status": "REVIEW",
                "message": (
                    "Potential sensitive information reference detected."
                ),
            }

        else:

            results["Safety"] = {
                "status": "PASS",
                "message": "No obvious secret patterns detected.",
            }

    else:

        results["Safety"] = {
            "status": "N/A",
            "message": "Strict safety evaluation was not enabled.",
        }

    return results