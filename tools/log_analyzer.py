import pandas as pd


BUSINESS_KEYWORDS = [
    "no files available",
    "business exception",
    "be002",
    "sftp"
]

TECHNICAL_KEYWORDS = [
    "selector",
    "timeout",
    "not found",
    "exception",
    "crash"
]


def classify_log_row(row: pd.Series) -> dict:
    """
    Classifies a single UiPath log row
    """
    message = str(row.get("Message", "")).lower()
    level = str(row.get("Level", "")).lower()

    # --- Business Exceptions ---
    if any(k in message for k in BUSINESS_KEYWORDS):
        return {
            "failure_type": "business_exception",
            "subcategory": "missing_input_files",
            "system": "sftp",
            "severity": "medium",
            "auto_retry": False,
            "confidence": 0.9,
            "recommended_action": "Check upstream SFTP feed and notify business"
        }

    # --- Technical Exceptions ---
    if any(k in message for k in TECHNICAL_KEYWORDS) and level in ["error", "fatal"]:
        return {
            "failure_type": "technical_exception",
            "subcategory": "application_or_ui_issue",
            "severity": "high",
            "auto_retry": False,
            "confidence": 0.75,
            "recommended_action": "Investigate application/UI change"
        }

    # --- Informational ---
    return {
        "failure_type": "info",
        "severity": "low",
        "auto_retry": False,
        "confidence": 0.3,
        "recommended_action": "No action required"
    }


def analyze_uipath_logs(csv_path: str) -> dict:
    """
    Analyzes full UiPath log CSV and returns agent-ready summary
    """
    df = pd.read_csv(csv_path)

    findings = []
    for _, row in df.iterrows():
        result = classify_log_row(row)
        if result["failure_type"] not in ["info"]:
            findings.append(result)

    if not findings:
        return {
            "status": "success",
            "message": "No critical failures detected"
        }

    # Pick the most confident failure
    root_cause = max(findings, key=lambda x: x["confidence"])

    return {
        "status": "failed",
        "root_cause": root_cause,
        "total_errors": len(findings)
    }
