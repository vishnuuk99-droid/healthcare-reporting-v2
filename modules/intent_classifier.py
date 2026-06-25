"""
Reporting Intent Engine – classifies CMS requirements into reporting
intent categories and recommends Power BI visual types.

Uses Gemini to analyze each requirement and determine whether it
calls for a Detail Listing, KPI, Trend Analysis, Comparison Analysis,
Cross Tabulation, Data Submission, Data Quality check, or Compliance
Monitoring visual.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from modules.schemas import ReportingIntent, ReportingIntentSet
from modules.file_manager import OUTPUT_DIR, KNOWLEDGE_DIR

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

_ANALYTICS_MODEL_FILE = OUTPUT_DIR / "analytics_model.json"
_INTENT_OUTPUT_FILE = OUTPUT_DIR / "reporting_intent.json"

VALID_INTENTS = [
    "single_metric",
    "time_series",
    "categorical_comparison",
    "distribution",
    "detailed_records",
    "grouped_summary",
]

_SYSTEM_INSTRUCTION = """\
You are a healthcare reporting analyst specialising in CMS data
reporting and analytical design. You will receive:

1. CMS reporting requirements (metrics, dimensions, filters, business
   rules, exclusions).
2. A star schema analytics model with fact/dimension tables and columns.
3. Organizational decisions from SME reviews.

For EACH distinct requirement (metrics, dimensions, business rules,
filters, exclusions — each individual item), classify its **reporting
intent** into exactly one of these analytical categories:

- **single_metric**: The requirement asks for a single summary number or indicator.
- **time_series**: The requirement asks for change or trends over time.
- **categorical_comparison**: The requirement asks to compare groups or categories.
- **distribution**: The requirement asks for proportional distribution of a whole.
- **detailed_records**: The requirement asks to list, enumerate, or display individual records.
- **grouped_summary**: The requirement asks for a pivot/matrix view grouped by multiple dimensions.

For each classified requirement produce:
- requirement: The exact requirement text.
- intent: One of the analytical categories above.
- required_columns: Which star schema columns are needed.
- reasoning: Brief explanation of why this intent was chosen.

Rules:
- Classify EVERY requirement item (each metric, dimension, filter,
  business rule, and exclusion as a separate entry).
- Use only the intent categories listed above.
- Reference only columns present in the star schema model.
- Apply organizational decisions when they affect terminology.
"""


def _get_client() -> genai.Client:
    """Create and return a configured Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY not found. "
            "Create a .env file in the project root with:\n"
            "GEMINI_API_KEY=your_key_here"
        )
    return genai.Client(api_key=api_key)


def _load_analytics_model() -> dict | None:
    """Load the saved analytics model."""
    if not _ANALYTICS_MODEL_FILE.exists():
        return None
    with open(_ANALYTICS_MODEL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_reporting_intents(
    requirements: dict,
    decisions: list[dict] | None = None,
) -> list[ReportingIntent]:
    """
    Classify CMS requirements into reporting intent categories.

    Args:
        requirements: The extracted CMS requirements dict.
        decisions: Organizational decisions list (optional).

    Returns:
        A list of validated ReportingIntent objects.
    """
    client = _get_client()
    analytics_model = _load_analytics_model()

    if not analytics_model:
        raise ValueError(
            "No analytics model found. Please generate and approve "
            "the analytics model on the Analytics Model page first."
        )

    # Build context
    context_parts = []

    context_parts.append(
        f"=== CMS REQUIREMENTS ===\n{json.dumps(requirements, indent=2)}"
    )

    structured_metrics = requirements.get("structured_metrics", [])
    if structured_metrics:
        context_parts.append(
            f"=== STRUCTURED METRIC DEFINITIONS ===\n"
            f"{json.dumps(structured_metrics, indent=2)}"
        )

    context_parts.append(
        f"=== STAR SCHEMA ANALYTICS MODEL ===\n"
        f"{json.dumps(analytics_model, indent=2)}"
    )

    if decisions:
        context_parts.append(
            f"=== ORGANIZATIONAL DECISIONS ===\n{json.dumps(decisions, indent=2)}"
        )

    content = "\n\n".join(context_parts)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=content,
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=ReportingIntentSet,
            temperature=0.2,
        ),
    )

    raw = json.loads(response.text)
    result = ReportingIntentSet.model_validate(raw)
    return result.intents


def save_reporting_intents(intents: list[dict]) -> str:
    """Persist approved reporting intents to output/reporting_intent.json."""
    _INTENT_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_INTENT_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(intents, f, indent=2, ensure_ascii=False)
    return str(_INTENT_OUTPUT_FILE.resolve())


def load_reporting_intents() -> list[dict] | None:
    """Load previously saved reporting intents."""
    if not _INTENT_OUTPUT_FILE.exists():
        return None
    with open(_INTENT_OUTPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
