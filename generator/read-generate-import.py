import argparse
import logging

from generator import generate_cards, validation
from generator.config import Config
from generator.entities import WordWithContext
from generator.input import read_input_file


def process_new_cards(input_words: list[WordWithContext]) -> None:
    generate_cards.generate_text(input_words)
    logging.info("Card generation completed")


def exclude_imported_words(
    input_words: list[WordWithContext], imported_existing_words: list[str]
) -> list[WordWithContext]:
    if len(imported_existing_words) >= 1:
        logging.info(
            f"Words {imported_existing_words} are imported from existing files "
            f"and are excluded from further processing"
        )
        return list(
            filter(
                lambda word_with_context: word_with_context.word
                not in imported_existing_words,
                input_words,
            )
        )
    return input_words


def main() -> None:
    # Create the parser
    parser = argparse.ArgumentParser(
        description=(
            "This tool processes the list of words or phrases (with optional context) "
            "and creates an Anki card for each word. "
        )
    )

    # Required positional arguments
    parser.add_argument(
        "input_file",
        type=str,
        help=(
            "Path to the input file, CSV with semicolons or Excel. "
            "Header [word;context] is required"
        ),
    )

    # Optional arguments
    parser.add_argument(
        "--processing_directory",
        type=str,
        help=(
            "Path of the directory where the data should be processed. "
            "It could be an empty directory. "
            "If directory contains generated cards, tool will suggest to import them."
        ),
        default=None,
    )
    parser.add_argument(
        "--openai_api_key",
        type=str,
        help=(
            "API key for OpenAI. "
            "If not set, the value from environment variable OPENAI_API_KEY is used"
        ),
        default=None,
    )
    parser.add_argument(
        "--deck_name",
        type=str,
        help="Name of the Anki deck. If not set, the default name is generated",
        default=None,
    )
    parser.add_argument(
        "--language",
        type=str,
        help=(
            "Target card language. Not only the card translation, "
            "customized generation process for each language"
        ),
        default=Config.DEFAULT_LANGUAGE,
        choices=Config.SUPPORTED_LANGUAGES,
    )
    parser.add_argument(
        "--level",
        type=str,
        help=(
            "Current language level, that should be used for card creation "
            "to avoid overcomplicated cards for beginners and vice versa"
        ),
        default=Config.DEFAULT_LEVEL,
        choices=Config.SUPPORTED_LEVELS,
    )
    parser.add_argument(
        "--dictionary_urls",
        help="Target dictionary urls",
        type=str,
        nargs="+",
        default=None,
    )
    parser.add_argument(
        "--quizlet_import_symbol_between_term_and_definition",
        help="See Quizlet import UI. Symbol between term and definition",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--quizlet_import_symbol_between_cards",
        help="See Quizlet import UI. Symbol between cards",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--cache_name",
        help=(
            "If you do not want to accidentally create multiple cards "
            "for the same word, you can store word in cache"
        ),
        type=str,
        default=None,
    )

    # Parse arguments
    args = parser.parse_args()

    # Setup config
    Config.setup_logging()
    Config.set_openai_key_or_use_default(args.openai_api_key)
    Config.set_processing_directory(args.processing_directory)
    Config.set_deck_name_or_use_default(args.deck_name)
    Config.set_language_or_use_default(args.language)
    Config.set_level_or_use_default(args.level)
    Config.set_dictionary_urls(args.dictionary_urls)
    Config.set_quizlet_import_symbol_between_term_and_definition(
        args.quizlet_import_symbol_between_term_and_definition
    )
    Config.set_quizlet_import_symbol_between_cards(
        args.quizlet_import_symbol_between_cards
    )
    Config.set_cache_name(args.cache_name)
    Config.setup_settings()

    # validate environment and read inputs
    validation.check_language()
    input_words: list[WordWithContext] = read_input_file.read_file_based_on_extension(
        args.input_file
    )

    # Processing
    input_words_except_imported = exclude_imported_words(input_words, [])
    process_new_cards(input_words_except_imported)
    logging.info("Processing completed")


if __name__ == "__main__":
    main()
