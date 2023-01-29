from .language import __language__

def is_valid_language(language: str) -> bool:
    return language == __language__