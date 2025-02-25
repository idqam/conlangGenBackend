from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models.schemas import PayloadSpec, PhonologySpec
from app.services.phonoGen import generate_valid_words, map_to_user_defined_form

router = APIRouter()

class WordResponse(BaseModel):
    words: List[str]
    originalPayload: PayloadSpec  # Include original payload in response

@router.post("/send-words-phonology", summary="After getting phonology from frontend, sends words back", response_model=WordResponse)
def send_words(payload: PayloadSpec):
    phonology = payload.phonology
    try:
        ipa_words = generate_valid_words(phonology, 200)
        if not ipa_words:
            raise HTTPException(status_code=400, detail="No words could be generated with the given phonology.")

        mapped_words = list(map_to_user_defined_form(ipa_words, phonology))

        return WordResponse(words=mapped_words, originalPayload=payload)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
