import logging

from generator.api_calls.text_prompt_by_language import (
    english_prompt_text,
    polish_prompt_text,
)
from generator.config import ENGLISH, POLISH, Config


def get_system_prompt_by_language() -> str | None:
    if Config.LANGUAGE == ENGLISH:
        return english_prompt_text.get_prompt()
    elif Config.LANGUAGE == POLISH:
        return polish_prompt_text.get_prompt()
    else:
        logging.error(f"No text prompt for language [{Config.LANGUAGE}]")
        return None
