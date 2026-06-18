import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP


DATA_PATH = Path(__file__).parent / "data" / "red_flags.json"
SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}
SEVERITY_SCORES = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 5,
}


mcp = FastMCP(
    name=os.getenv("MCP_SERVER_NAME", "medical-mcp-server"),
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "23000")),
)


def _load_red_flags() -> dict:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        return json.load(data_file)


def _normalize_severity(severities: list[str]) -> str:
    if not severities:
        return "low"

    return max(severities, key=lambda severity: SEVERITY_ORDER.get(severity, 0))


@mcp.tool()
def check_red_flags(symptoms: list[str]) -> dict:
    data = _load_red_flags()
    detected = []
    severities = []

    for symptom in symptoms:
        normalized_symptom = symptom.lower().strip()
        entry = data.get(normalized_symptom)
        if not entry:
            continue

        severities.append(entry["severity"])
        if entry["red_flag"]:
            detected.append(
                {
                    "symptom": normalized_symptom,
                    "severity": entry["severity"],
                }
            )

    return {
        "red_flags_detected": detected,
        "severity": _normalize_severity(severities),
        "requires_attention": bool(detected),
    }


@mcp.tool()
def symptom_severity(symptoms: list[str]) -> dict:
    data = _load_red_flags()
    score = 0

    for symptom in symptoms:
        normalized_symptom = symptom.lower().strip()
        entry = data.get(normalized_symptom)
        if not entry:
            continue

        score += SEVERITY_SCORES.get(entry["severity"], 0)

    if score <= 3:
        severity = "low"
    elif score <= 6:
        severity = "medium"
    elif score <= 10:
        severity = "high"
    else:
        severity = "critical"

    return {
        "score": score,
        "severity": severity,
    }


@mcp.tool()
def emergency_recommendation(severity: str) -> dict:
    recommendations = {
        "low": "Surveillance simple recommandée.",
        "medium": "Consultation médicale recommandée si aggravation.",
        "high": "Consultation rapide recommandée.",
        "critical": "Orientation urgente vers une prise en charge médicale.",
    }

    return {
        "recommendation": recommendations.get(
            severity,
            "Surveillance simple recommandée.",
        )
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
