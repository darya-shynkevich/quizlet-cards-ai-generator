import logging
import random
import time

from generator.api_calls import openai_text
from generator.config import Config
from generator.entities import CardRawDataV1, WordWithContext
from generator.input.file_operations import generate_card_data_path, save_text


def generate_text(
    input_words: list[WordWithContext],
) -> dict[WordWithContext, CardRawDataV1]:
    words_total = len(input_words)
    words_remaining = words_total

    logging.info(
        f"Starting generation of text for {words_total} words "
        f"{list(map(lambda entry: entry.word, input_words))}"
    )
    words_cards: dict[WordWithContext, CardRawDataV1] = {}

    processed_worlds = []
    for word_with_context in input_words:
        try:
            card_raw = create_card_for_word(word_with_context)
            words_cards[word_with_context] = card_raw
            logging.info(f"Word [{word_with_context.word}] processed")
        except Exception as e:
            logging.exception(
                f"Failed to process word [{word_with_context.word}] due to [{e}]"
            )
            logging.warning(f"Word [{word_with_context.word}] will be skipped")
        else:
            processed_worlds.append(word_with_context.word + "\n")
        words_remaining -= 1
        if words_remaining > 0:
            wait_after_word_processing()

    with open(Config.CACHE_NAME, "a") as cache_file:  # type: ignore
        cache_file.writelines(processed_worlds)

    return words_cards


def create_card_for_word(word_with_context: WordWithContext) -> CardRawDataV1:
    card_text = openai_text.chat_generate_text(word_with_context)
    logging.info(f"Card text is created for {word_with_context}")

    card_raw: CardRawDataV1 = CardRawDataV1(
        word=word_with_context.word.lower(), card_text=card_text
    )
    card_data_path = generate_card_data_path(
        Config.PROCESSING_DIRECTORY_PATH, Config.DECK_NAME  # type: ignore
    )
    save_text(card_raw, card_data_path)
    return card_raw


def wait_after_word_processing() -> None:
    sleep_seconds = random.randint(1, 20)  # nosec CWE-330
    logging.info(f"Waiting [{sleep_seconds}] seconds after word processing (API RPM)")
    time.sleep(sleep_seconds)
