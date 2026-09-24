import json
import os

from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session
from .forecast_service import (
    dissolved_oxygen_warning,
    ammonia_warning,
)

from .pond_context_service import get_pond_context


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in the .env file."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def ask_pond_assistant(
    db: Session,
    pond_name: str,
    question: str,
):
    """
    Answer questions using pond-specific data.
    """

    # Get grounded pond data
    context = get_pond_context(
        db,
        pond_name,
    )

    if context.get("status") != "OK":
        return context

    # Convert datetime objects safely for Gemini
    context_json = json.dumps(
        context,
        default=str,
        indent=2,
    )

    prompt = f"""
You are Aqua Copilot, an AI assistant for shrimp pond monitoring.

Your job is to help farmers understand pond conditions using ONLY
the pond data supplied below.

Important rules:
- Base your answer on the supplied pond data.
- Do not invent sensor readings or pond conditions.
- Clearly identify critical water-quality problems.
- Prioritize immediate safety actions when conditions are critical.
- Explain the reasoning in simple language.
- Use recent readings and alerts when answering.
- If the available data cannot answer the question, say so.
- Do not claim that AI predictions are guaranteed.
- Keep the answer practical and concise.

POND DATA:
{context_json}

USER QUESTION:
{question}

Provide a clear pond-specific answer.
"""

    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
    ]

    last_error = None

    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            return {
                "status": "OK",
                "pond_name": pond_name,
                "question": question,
                "model": model_name,
                "answer": response.text,
            }

        except Exception as error:
            last_error = error
            continue

    return {
        "status": "ERROR",
        "message": (
            "The AI service is temporarily unavailable. "
            "Please try again shortly."
        ),
        "details": str(last_error),
    }
