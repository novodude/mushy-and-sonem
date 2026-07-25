"""
core/ai.py — talks to the model router, falling through a list of models if one is
overloaded (503) or otherwise erroring. Also handles vision (image) prompts.
"""

import asyncio
import os

import dotenv
from openai import AsyncOpenAI

NARA_API_KEY = dotenv.get_key(".env", "NARA_API_KEY") or os.getenv("NARA_API_KEY")
ROUTER_BASE_URL = dotenv.get_key(".env", "ROUTER_BASE_URL") or "https://router.bynara.id/v1"

# Tried in order. If a model 503s (overloaded) or otherwise fails, we fall through to
# the next one rather than failing the whole turn.
MODEL_FALLBACKS = [
    "mistral-large",
    "ling-3.0-flash-free",
    "laguna-s-2.1",
]

RETRIES_PER_MODEL = 2
RETRY_BACKOFF_SECONDS = 2


def _is_retryable(exc: Exception) -> bool:
    status = getattr(exc, "status_code", None)
    return status == 503 or status == 429 or status is None


async def generate_response(messages: list[dict], models: list[str] | None = None) -> str:
    """
    Try each model in `models` (defaults to MODEL_FALLBACKS) in order. Within each
    model, retry a couple times on 503/429 with a short backoff before moving on to
    the next model. Raises the last error only if every model in the chain failed.
    """
    models = models or MODEL_FALLBACKS
    last_error: Exception | None = None

    async with AsyncOpenAI(base_url=ROUTER_BASE_URL, api_key=NARA_API_KEY) as client:
        for model in models:
            for attempt in range(RETRIES_PER_MODEL):
                try:
                    res = await client.chat.completions.create(model=model, messages=messages)
                    return res.choices[0].message.content
                except Exception as e:
                    last_error = e
                    status = getattr(e, "status_code", None)
                    print(f"[ai] {model} attempt {attempt + 1} failed (status={status}): {e}")
                    if not _is_retryable(e):
                        break  # don't retry something like a 400 (bad request) — move to next model
                    await asyncio.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))

    raise RuntimeError(f"All models in the fallback chain failed. Last error: {last_error}")


async def describe_image(image_url: str, question: str = "Describe this image.") -> str:
    """Vision — ask a model about an image URL. Falls through the same model chain."""
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": image_url}},
        ],
    }]
    return await generate_response(messages)
