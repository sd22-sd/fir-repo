from src.core.groq_client import call_llm
from .prompt_builder import build_pass1_prompt
from .json_enforcer import safe_parse_json, enforce_schema


def run_pass1(text):

    prompt = build_pass1_prompt(text)

    try:

        response = call_llm(prompt, max_tokens=3000)

        parsed = safe_parse_json(response)

        if not parsed:
            raise Exception("Pass 1: JSON parsing failed.")

        structured = enforce_schema(parsed)

        return structured

    except Exception as e:

        print("❌ PASS1 ERROR:")
        print(str(e))

        raise