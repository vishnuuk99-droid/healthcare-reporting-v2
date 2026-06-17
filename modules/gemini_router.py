"""
Gemini Router – handles model failover (quota/spikes) within the Gemini API.

Provides automatic failover across different Gemini models (e.g. 2.0-flash,
1.5-flash, 1.5-pro) when encountering quota limits (429) or transient server
errors (503).
"""

import os
import time
import logging
from typing import Optional, Any
from google import genai
from google.genai import types
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# List of Gemini models to attempt in order of preference/speed
GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

def _get_client() -> genai.Client:
    """Create and return a configured Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY not found. Please set GEMINI_API_KEY in your .env file."
        )
    return genai.Client(api_key=api_key)

def generate_content(
    contents: Any,
    system_instruction: str,
    response_schema: Optional[type[BaseModel]] = None,
    temperature: float = 0.2,
    task_label: str = "Processing"
) -> Any:
    """
    Call Gemini's generate_content with failover across models.
    Updates the active Streamlit spinner/status label if available.
    """
    client = _get_client()
    last_error = None

    # Try importing streamlit dynamically to update the status container
    st = None
    try:
        import streamlit as _st
        st = _st
    except ImportError:
        pass

    for model in GEMINI_MODELS:
        # Update the Streamlit status container if active
        if st and "active_status_container" in st.session_state:
            status = st.session_state["active_status_container"]
            status.update(label=f"⏳ {task_label} with **{model}**...")

        try:
            logger.info(f"Attempting task '{task_label}' with model: {model}")
            
            # Build configuration
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature
            )
            if response_schema:
                config.response_mime_type = "application/json"
                config.response_schema = response_schema

            # Call API
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
            return response

        except Exception as e:
            last_error = e
            err_str = str(e).lower()
            
            # Check if error is quota exceeded (429) or service unavailable (503)
            # or rate limit errors
            is_quota_or_spike = any(
                keyword in err_str
                for keyword in ["quota", "exhausted", "503", "unavailable", "429", "resource_exhausted", "limit"]
            )
            
            if is_quota_or_spike:
                logger.warning(f"Model {model} failed due to quota/spike. Error: {e}. Failing over...")
                if st:
                    st.warning(f"⚠️ **{model}** failed (quota/overload). Failing over to the next model...")
                time.sleep(1)  # Brief pause before retry/failover
                continue
            else:
                # For validation or schema errors, raise immediately
                raise e

    raise Exception(
        f"All configured Gemini models failed. Last error: {last_error}"
    )
