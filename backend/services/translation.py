
import torch
from functools import lru_cache

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor


LANGUAGES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "te": "tel_Telu",
    "gu": "guj_Gujr",
}

EN_TO_INDIC_MODEL = "ai4bharat/indictrans2-en-indic-dist-200M"
INDIC_TO_EN_MODEL = "ai4bharat/indictrans2-indic-en-dist-200M"


def get_device():
    # Start with CPU for a reliable compatibility test.
    # We can enable Apple MPS after successful inference.
    return torch.device("cpu")


@lru_cache(maxsize=2)
def load_translation_model(direction):

    if direction == "en_to_indic":
        model_name = EN_TO_INDIC_MODEL
    elif direction == "indic_to_en":
        model_name = INDIC_TO_EN_MODEL
    else:
        raise ValueError("Invalid translation direction.")

    device = get_device()

    print(f"\nLoading model: {model_name}")
    print(f"Device: {device}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        trust_remote_code=True
    )

    model = model.to(device)
    model.eval()

    processor = IndicProcessor(inference=True)

    print("Translation model loaded successfully.")

    return tokenizer, model, processor, device


def translate_one_step(text, source_code, target_code, direction):

    tokenizer, model, processor, device = load_translation_model(direction)

    prepared_text = processor.preprocess_batch(
        [text],
        src_lang=source_code,
        tgt_lang=target_code
    )

    if not prepared_text or not prepared_text[0]:
        raise RuntimeError("Text preprocessing returned an empty result.")

    print("Preprocessing completed.")

    inputs = tokenizer(
        prepared_text,
        truncation=True,
        padding="longest",
        max_length=256,
        return_tensors="pt",
        return_attention_mask=True
    )

    if inputs.get("attention_mask") is None:
        raise RuntimeError("Tokenizer did not generate an attention mask.")

    inputs = inputs.to(device)

    print("Tokenization completed. Generating translation...")

    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=3,
            num_return_sequences=1
        )

    generated_tokens = tokenizer.batch_decode(
        generated_tokens.detach().cpu().tolist(),
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )

    final_text = processor.postprocess_batch(
        generated_tokens,
        lang=target_code
    )

    if not final_text:
        raise RuntimeError("The model returned an empty translation.")

    print("Translation completed successfully.")

    return final_text[0]


def translate_text(text, source_language, target_language):

    if not isinstance(text, str):
        raise TypeError("Input must be text.")

    text = text.strip()

    if not text:
        raise ValueError("Please enter some text.")

    if source_language not in LANGUAGES:
        raise ValueError("Unsupported source language.")

    if target_language not in LANGUAGES:
        raise ValueError("Unsupported target language.")

    if source_language == target_language:
        return text

    source_code = LANGUAGES[source_language]
    target_code = LANGUAGES[target_language]

    if source_language == "en":
        return translate_one_step(
            text,
            source_code,
            target_code,
            "en_to_indic"
        )

    if target_language == "en":
        return translate_one_step(
            text,
            source_code,
            target_code,
            "indic_to_en"
        )

    # Indian language -> English -> another Indian language
    english_text = translate_one_step(
        text,
        source_code,
        "eng_Latn",
        "indic_to_en"
    )

    return translate_one_step(
        english_text,
        "eng_Latn",
        target_code,
        "en_to_indic"
    )
