
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

SUPPORTED_LANGUAGES = {
    "hi": {
        "name": "Hindi",
        "script": sanscript.DEVANAGARI
    },
    "te": {
        "name": "Telugu",
        "script": sanscript.TELUGU
    },
    "gu": {
        "name": "Gujarati",
        "script": sanscript.GUJARATI
    }
}


def get_supported_languages():
    return {
        code: details["name"]
        for code, details in SUPPORTED_LANGUAGES.items()
    }


def transliterate_text(text, language_code):
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text = text.strip()

    if not text:
        raise ValueError("Please enter some text.")

    if language_code not in SUPPORTED_LANGUAGES:
        raise ValueError("Unsupported transliteration language.")

    target_script = SUPPORTED_LANGUAGES[language_code]["script"]

    return transliterate(
        text,
        sanscript.ITRANS,
        target_script
    )
