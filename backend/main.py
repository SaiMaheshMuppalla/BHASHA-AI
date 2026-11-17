
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.services.transliteration import (
    transliterate_text,
    get_supported_languages
)
from backend.services.translation import translate_text


app = FastAPI(
    title="BHASHA AI",
    description="Indian Multilingual NLP Assistant",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ConversionRequest(BaseModel):
    text: str
    mode: str
    source_language: str = "en"
    target_language: str = "hi"


@app.get("/")
def home():
    return {
        "message": "Welcome to BHASHA AI!",
        "status": "running",
        "version": "2.0.0"
    }


@app.get("/languages")
def languages():
    return {
        "translation": {
            "en": "English",
            "hi": "Hindi",
            "te": "Telugu",
            "gu": "Gujarati"
        },
        "transliteration": get_supported_languages()
    }


@app.post("/convert")
def convert(request: ConversionRequest):
    try:
        if request.mode == "transliteration":
            result = transliterate_text(
                request.text,
                request.target_language
            )

        elif request.mode == "translation":
            result = translate_text(
                request.text,
                request.source_language,
                request.target_language
            )

        else:
            raise ValueError(
                "Mode must be translation or transliteration."
            )

        return {
            "input": request.text,
            "mode": request.mode,
            "source_language": request.source_language,
            "target_language": request.target_language,
            "output": result
        }

    except (ValueError, TypeError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        print("\n========== BHASHA AI ERROR ==========")
        traceback.print_exc()
        print("=====================================\n")

        raise HTTPException(
            status_code=500,
            detail=f"Conversion failed: {str(error)}"
        )
