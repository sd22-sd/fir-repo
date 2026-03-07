# src/core/groq_client.py

import os
import time
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=GROQ_API_KEY)


def call_llm(
    prompt: str,
    max_tokens: int = 1200,
    temperature: float = 0,
    retries: int = 2
) -> str:
    """
    Call Groq LLM (llama-3.1-8b-instant) with retry mechanism.
    Designed for structured JSON extraction.
    """

    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert Indian FIR document analyst. "
                            "Always return STRICT JSON when requested. "
                            "Do not include explanations. "
                            "Do not include markdown."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            if attempt < retries:
                print(f"LLM call failed (attempt {attempt + 1}). Retrying...")
                time.sleep(1)
            else:
                raise RuntimeError(f"Groq API failed after retries: {str(e)}")