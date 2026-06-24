"""
Gemini API client for CMS requirement extraction.

Uses the google-genai SDK with structured output to produce
validated JSON conforming to the CMSRequirements schema.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from modules.schemas import CMSRequirements

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

# ── System prompt ────────────────────────────────────────────────────
_SYSTEM_INSTRUCTION = """\
You are a healthcare regulatory analyst AI. Your job is to read CMS
(Centers for Medicare & Medicaid Services) documents and extract
structured reporting requirements.

Analyze the provided document text carefully and extract:
- report_name: The official name or title of the report.
- report_type: The category (quality measure, cost report, enrollment, etc.).
- reporting_entities: Who must submit this report.
- metrics: All quantitative measures, KPIs, or data points required.
- dimensions: Grouping/segmentation axes (state, provider type, time period, etc.).
- filters: Criteria that narrow the data population.
- business_rules: Calculations, conditional logic, or validation rules.
- exclusions: Populations or data explicitly excluded from the report.
- reporting_frequency: Submission cadence (monthly, quarterly, annually, etc.).
- notes: Any additional caveats, context, or observations.

Be thorough. Extract every requirement you can identify from the text.
If a field has no relevant information in the document, leave it as an
empty string or empty list as appropriate.

Additionally, for EACH metric identified above, also produce a structured
decomposition in the 'structured_metrics' list:

- metric_name: Exactly matching the metric string in the 'metrics' list.
- metric_type: Count, Sum, Average, Percentage, Ratio, or Distinct Count.
- business_definition: What this metric measures and why.
- numerator: The population/value being counted or summed.
  Example: "Grievances where the MAO provided a decision during the
  reporting period, excluding dismissed and withdrawn grievances."
- denominator: The denominator population. Empty for Count/Sum metrics.
- inclusion_rules: Criteria records MUST meet.
- exclusion_rules: Criteria that exclude records.
- timeliness_days: Regulatory threshold in days (0 if not applicable).
- reporting_period_type: Exactly one of: Quarterly, Annual, Monthly, PointInTime.
- period_anchor: The date field (e.g., decision_date, notification_date,
  enrollment_date, payment_date, appeal_date).
- cms_element_reference: CMS element/section ref (e.g., "Element A").
- confidence_score: Float 0.0-1.0. Use 1.0 for clearly defined metrics,
  0.8 for metrics with minor ambiguity, 0.5 for metrics requiring
  significant interpretation.
- extraction_notes: Your reasoning and assumptions while interpreting
  this metric.

Important: The structured_metrics list must have ONE entry for EVERY
metric in the metrics list. Do not skip any metric.
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


def extract_requirements(document_text: str) -> CMSRequirements:
    """
    Send CMS document text to Gemini and return structured requirements.

    Args:
        document_text: The full extracted text from a CMS PDF.

    Returns:
        A validated CMSRequirements Pydantic model instance.

    Raises:
        EnvironmentError: If GEMINI_API_KEY is not set.
        Exception: If Gemini returns an unparsable response.
    """
    client = _get_client()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=document_text,
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=CMSRequirements,
            temperature=0.2,
        ),
    )

    # Parse and validate through Pydantic
    raw_json = json.loads(response.text)
    return CMSRequirements.model_validate(raw_json)


def save_requirements(requirements: CMSRequirements, output_path: str | Path) -> str:
    """
    Persist extracted requirements to a JSON file.

    Args:
        requirements: Validated CMSRequirements instance.
        output_path: File path to write the JSON to.

    Returns:
        The absolute path of the saved file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(requirements.model_dump_json(indent=2))

    return str(output_path.resolve())
