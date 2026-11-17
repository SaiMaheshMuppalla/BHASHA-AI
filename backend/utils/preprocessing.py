
import re
import unicodedata


def clean_text(text):
    """
    Normalize and clean multilingual text.
    Preserves Indian language characters.
    """

    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # Convert English uppercase to lowercase
    text = text.lower()

    # Remove punctuation while preserving letters and spaces
    text = re.sub(r"[^\w\s]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize_text(text):
    """
    Basic whitespace tokenization.
    """

    return text.split()


def preprocess_text(text):

    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)

    return cleaned, tokens


if __name__ == "__main__":

    sentences = [
        "Hello! I am learning NLP.",
        "मुझे आर्टिफिशियल इंटेलिजेंस सीखना है।",
        "నాకు NLP నేర్చుకోవాలి.",
        "મારે NLP શીખવું છે."
    ]

    for sentence in sentences:

        cleaned, tokens = preprocess_text(sentence)

        print("\nOriginal:", sentence)
        print("Cleaned:", cleaned)
        print("Tokens:", tokens)
        print("-" * 50)
