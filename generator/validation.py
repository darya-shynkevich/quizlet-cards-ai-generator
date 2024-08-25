from generator.config import Config


def check_language() -> None:
    if Config.LANGUAGE not in Config.SUPPORTED_LANGUAGES:
        raise Exception(f"Language {Config.LANGUAGE} is not supported")


def check_level() -> None:
    if Config.LEVEL not in Config.SUPPORTED_LEVELS:
        raise Exception(f"Language level {Config.LEVEL} is not supported")
