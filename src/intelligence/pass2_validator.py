from src.core.groq_client import call_llm
from .json_enforcer import safe_parse_json, enforce_schema
import json

CHUNK_SIZE = 1200  # characters per chunk


def split_text(text, size):
    return [text[i:i + size] for i in range(0, len(text), size)]


def merge_json(base, new):
    """
    Merge validated JSON fields.
    Prefer new values if they are non-empty.
    Handles lists of dicts safely.
    """

    for key, value in new.items():

        # Nested dict → recursive merge
        if isinstance(value, dict):
            base[key] = merge_json(base.get(key, {}), value)

        # List values
        elif isinstance(value, list):

            if not value:
                continue

            if not base.get(key):
                base[key] = value
                continue

            if isinstance(value[0], dict):
                base[key].extend(value)
            else:
                combined = base.get(key, []) + value
                base[key] = list(set(combined))

        # Scalar values
        else:
            if value not in [None, "", "Unknown"]:
                base[key] = value

    return base


def run_pass2(original_text, structured_json):

    chunks = split_text(original_text, CHUNK_SIZE)

    validated_json = structured_json

    # 🔒 preserve original occurrence datetime
    original_occurrence = structured_json.get("incident", {}).get("occurrence_datetime")

    for chunk in chunks:

        prompt = f"""
You are validating structured FIR data.

Compare the structured JSON with the FIR text.

Tasks:
- Correct wrong dates
- Remove hallucinated values
- Ensure numbers match the document
- Ensure vehicle numbers match the document
- Do NOT invent information

IMPORTANT:
Do NOT modify the field 'occurrence_datetime'.

Return corrected JSON only.

FIR TEXT:
\"\"\"
{chunk}
\"\"\"

CURRENT STRUCTURED JSON:
{json.dumps(validated_json, ensure_ascii=False)}
"""

        response = call_llm(prompt, max_tokens=400)

        parsed = safe_parse_json(response)

        if parsed:
            validated_json = merge_json(validated_json, parsed)

            # 🔒 enforce protection again after merge
            if original_occurrence:
                validated_json.setdefault("incident", {})[
                    "occurrence_datetime"
                ] = original_occurrence

    validated_json = enforce_schema(validated_json)

    return validated_json