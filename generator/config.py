import logging
import os
import uuid

ENGLISH = "english"
POLISH = "polish"

A1 = "A1"
A2 = "A2"
B1 = "B1"
B2 = "B2"
C1 = "C1"
C2 = "C2"


class Config:
    OPENAI_API_KEY: str | None = None
    DECK_NAME: str = "my_deck"

    SUPPORTED_LANGUAGES: list[str] = [ENGLISH, POLISH]
    DEFAULT_LANGUAGE: str = ENGLISH
    LANGUAGE: str | None = None

    SUPPORTED_LEVELS: list[str] = [A1, A2, B1, B2, C1, C2]
    DEFAULT_LEVEL: str = C1
    LEVEL: str | None = None

    DICTIONARY_URLS: list[str] = []

    QUIZLET_IMPORT_SYMBOL_BETWEEN_TERM_AND_DEFINITION: str = ","
    QUIZLET_IMPORT_SYMBOL_BETWEEN_CARDS: str = ";;;\n\n"

    PROCESSING_DIRECTORY_PATH: str | None = None

    CACHE_NAME: str | None = None

    @classmethod
    def setup_openai_api_key_from_environment(cls) -> None:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key is None:
            raise EnvironmentError("OPENAI_API_KEY environment variable is not set")
        cls.OPENAI_API_KEY = openai_api_key
        logging.info("OPENAI_API_KEY set from environment variable")

    @classmethod
    def set_openai_key_or_use_default(cls, api_key: str) -> None:
        if api_key is None:
            cls.setup_openai_api_key_from_environment()
        else:
            cls.OPENAI_API_KEY = api_key

    @classmethod
    def set_processing_directory(cls, processing_directory: str) -> None:
        if processing_directory is not None:
            cls.PROCESSING_DIRECTORY_PATH = processing_directory

    @classmethod
    def set_deck_name_or_use_default(cls, deck_name: str) -> None:
        if deck_name is None:
            cls.DECK_NAME = f"default_deck_name_{uuid.uuid4()}"
        else:
            cls.DECK_NAME = deck_name

    @classmethod
    def set_language_or_use_default(cls, language: str) -> None:
        if language is None:
            cls.LANGUAGE = cls.DEFAULT_LANGUAGE
        elif language.lower() in cls.SUPPORTED_LANGUAGES:
            cls.LANGUAGE = language.lower()
        else:
            raise Exception(
                f"Language [{language}] not supported. "
                f"Supported languages: {cls.SUPPORTED_LANGUAGES}"
            )
        logging.info(f"Language set to [{cls.LANGUAGE}]")

    @classmethod
    def set_level_or_use_default(cls, level: str) -> None:
        if level is None:
            cls.LEVEL = cls.DEFAULT_LEVEL
        elif level.upper() in cls.SUPPORTED_LEVELS:
            cls.LEVEL = level.upper()
        else:
            raise Exception(
                f"Language level [{level}] not supported. "
                f"Supported language levels: {cls.SUPPORTED_LEVELS}"
            )
        logging.info(f"Language level set to [{cls.LEVEL}]")

    @classmethod
    def set_dictionary_urls(cls, dictionary_urls: list[str]) -> None:
        if dictionary_urls is not None:
            cls.DICTIONARY_URLS = dictionary_urls

    @classmethod
    def set_quizlet_import_symbol_between_term_and_definition(cls, symbol: str) -> None:
        if symbol is not None:
            cls.QUIZLET_IMPORT_SYMBOL_BETWEEN_TERM_AND_DEFINITION = symbol

    @classmethod
    def set_quizlet_import_symbol_between_cards(cls, symbol: str) -> None:
        if symbol is not None:
            cls.QUIZLET_IMPORT_SYMBOL_BETWEEN_CARDS = symbol

    @classmethod
    def set_cache_name(cls, cache_name: str) -> None:
        if cache_name is not None:
            cls.CACHE_NAME = f"{cache_name}.txt"

    @classmethod
    def setup_logging(cls) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        logging.info("Logger configured")

    @classmethod
    def setup_settings(cls) -> None:
        if cls.PROCESSING_DIRECTORY_PATH is None:
            cls.PROCESSING_DIRECTORY_PATH = f"./output/{cls.LANGUAGE}"

        if cls.CACHE_NAME is None:
            cls.CACHE_NAME = f"./cache/{cls.LANGUAGE}.txt"
