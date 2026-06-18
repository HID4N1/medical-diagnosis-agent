import asyncio

from app.tools.mcp_client import analyze_symptoms


if __name__ == "__main__":
    symptoms = [
        "fatigue",
        "high fever",
    ]

    result = asyncio.run(analyze_symptoms(symptoms))
    print(result)
