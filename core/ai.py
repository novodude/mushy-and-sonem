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
    "nemotron-3-ultra",
    "laguna-s-2.1"
]

RETRIES_PER_MODEL = 3
RETRY_BACKOFF_SECONDS = 2


class AllModelsFailedError(Exception):
    """Raised when every model in the fallback chain failed — whether that's an
    actual quota/rate-limit exhaustion or every provider just being down. Either way
    the right move is the same: stop hammering and back off for a while."""


async def generate_response(
    messages: list[dict],
    models: list[str] | None = None,
) -> str:
    models = models or MODEL_FALLBACKS
    last_error: Exception | None = None

    async with AsyncOpenAI(
        base_url=ROUTER_BASE_URL,
        api_key=NARA_API_KEY,
    ) as client:
        for model in models:
            for attempt in range(RETRIES_PER_MODEL):
                try:
                    res = await client.chat.completions.create(
                        model=model,
                        messages=messages,
                    )
                    return res.choices[0].message.content

                except Exception as exc:
                    last_error = exc
                    status = getattr(exc, "status_code", None)

                    print(
                        f"[ai] {model} attempt {attempt + 1} "
                        f"failed (status={status}): {exc}"
                    )

                    # Rate limit: don't waste more requests.
                    if status == 429:
                        await asyncio.sleep(
                            RETRY_BACKOFF_SECONDS * (attempt + 1)
                        )
                        continue

                    # Invalid/unavailable model: skip immediately.
                    if status == 400:
                        break

                    # Only retry temporary overloads.
                    if status == 503:
                        await asyncio.sleep(
                            RETRY_BACKOFF_SECONDS * (attempt + 1)
                        )
                        continue

                    # Unknown errors: move to next model.
                    break

    raise AllModelsFailedError(str(last_error))


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
