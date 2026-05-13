import os
import time
import logging
from openai import OpenAI
from typing import Optional

from utils.logger import get_logger

logger = get_logger(__name__)

def _create_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)

def call_llm(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.5, max_retries: int = 3) -> str:
    client = _create_client()
    last_error = None

    for attempt in range(max_retries):
        try:
            logger.info(f"Calling LLM (attempt {attempt + 1}/{max_retries})")
            res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            content = res.choices[0].message.content
            if not content:
                raise RuntimeError("LLM returned empty response")
            return content
        except Exception as e:
            last_error = e
            logger.warning(f"LLM call failed: {e}")
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                logger.info(f"Retrying in {wait}s...")
                time.sleep(wait)

    raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_error}")
