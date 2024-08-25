import logging
import os

from generator.config import Config
from generator.entities import CardRawDataV1


def save_text(content: CardRawDataV1, path: str) -> None:
    _content = (
        f"{content.word}{Config.QUIZLET_IMPORT_SYMBOL_BETWEEN_TERM_AND_DEFINITION}{content.card_text}".replace(
            '""', '"'
        )
        .replace(',"', ",")
        .replace("*", "Examples:")
        .replace("[", "")
        .replace("]", "")
    )

    with open(path, "a+") as output_file:
        output_file.write(_content + Config.QUIZLET_IMPORT_SYMBOL_BETWEEN_CARDS)

    logging.debug(f"Text for {content.word} saved as {path}")


def generate_card_data_path(processing_directory_path: str, filename: str) -> str:
    return os.path.join(processing_directory_path, filename + ".txt")
