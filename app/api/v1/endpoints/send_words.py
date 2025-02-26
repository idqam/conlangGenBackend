import random
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models.schemas import PayloadSpec, PhonologySpec
from app.services.phonoGen import generate_valid_words, map_to_user_defined_form

router = APIRouter()

class WordResponse(BaseModel):
    words: List[str]
    originalPayload: PayloadSpec 

def assign_default_frequencies(phonology: PhonologySpec):
    if phonology.activeVowels and (not phonology.vowelFrequencies or not phonology.vowelFrequencies.keys()):
        freq = {v: random.random() for v in phonology.activeVowels}
        total = sum(freq.values())
        phonology.vowelFrequencies = {k: v / total for k, v in freq.items()}
    if phonology.activeConsonants and (not phonology.consonantFrequencies or not phonology.consonantFrequencies.keys()):
        freq = {c: random.random() for c in phonology.activeConsonants}
        total = sum(freq.values())
        phonology.consonantFrequencies = {k: v / total for k, v in freq.items()}

@router.post(
    "/send-words-phonology",
    summary="After getting phonology from frontend, sends words back",
    response_model=WordResponse
)
def send_words(payload: PayloadSpec):
    phonology = payload.phonology

    assign_default_frequencies(phonology)
    
    try:
        ipa_words = generate_valid_words(phonology, 400) 
        
        if not ipa_words:
            raise HTTPException(status_code=400, detail="No words could be generated with the given phonology.")

        mapped_words = list(map_to_user_defined_form(ipa_words, phonology))

        return WordResponse(words=mapped_words, originalPayload=payload)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
