import json
import os

from langchain_mcp_adapters.client import MultiServerMCPClient


SEVERITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


async def get_medical_tools():
    mcp_client = MultiServerMCPClient(
        {
            "medical_server": {
                "transport": "streamable_http",
                "url": os.getenv("MCP_SERVER_URL", "http://localhost:23000/mcp"),
            }
        }
    )
    return await mcp_client.get_tools()


def _parse_tool_result(result):
    if isinstance(result, dict):
        return result

    if isinstance(result, list) and result:
        first_item = result[0]
        if isinstance(first_item, dict):
            text = first_item.get("text")
            if isinstance(text, str):
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"value": text}

        return {"value": result}

    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"value": result}

    content = getattr(result, "content", None)
    if isinstance(content, str):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"value": content}

    return result


def _max_severity(*severities: str) -> str:
    valid_severities = [
        severity for severity in severities if severity in SEVERITY_ORDER
    ]
    if not valid_severities:
        return "low"

    return max(
        valid_severities,
        key=lambda severity: SEVERITY_ORDER[severity],
    )


def _find_tool(tools: list, tool_name: str):
    for tool in tools:
        if getattr(tool, "name", None) == tool_name:
            return tool

    raise ValueError(f"MCP tool not found: {tool_name}")


async def analyze_symptoms(symptoms: list[str]) -> dict:
    tools = await get_medical_tools()
    check_red_flags_tool = _find_tool(tools, "check_red_flags")
    symptom_severity_tool = _find_tool(tools, "symptom_severity")
    emergency_recommendation_tool = _find_tool(tools, "emergency_recommendation")

    red_flags = _parse_tool_result(
        await check_red_flags_tool.ainvoke({"symptoms": symptoms})
    )
    severity_result = _parse_tool_result(
        await symptom_severity_tool.ainvoke({"symptoms": symptoms})
    )
    severity = _max_severity(
        severity_result.get("severity", "low"),
        red_flags.get("severity", "low"),
    )
    recommendation = _parse_tool_result(
        await emergency_recommendation_tool.ainvoke({"severity": severity})
    )

    return {
        "red_flags": red_flags,
        "severity": severity,
        "recommendation": recommendation.get(
            "recommendation",
            "Surveillance simple recommandée.",
        ),
        "score": severity_result.get("score", 0),
        "symptoms": symptoms,
    }
