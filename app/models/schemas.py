from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional

class PhonoTest(BaseModel):
    activeVowels: Optional[List[str]]
    activeConsonants: Optional[List[str] ]

class AdditionalFeatureSpec(BaseModel):
    grammaticalGender: Optional[str] = ""
    negation: Optional[str] = ""
    pronounSystem: Optional[str] = ""

class GrammarSpec(BaseModel):
    morphology: Optional[str] = ""
    wordOrder: Optional[str] = ""
    nounCases: Optional[str] = ""
    definedNounCases: Optional[str] = ""
    verbConjugation: Optional[str] = ""
    verbTenses: List[str] = []
    verbAspects: List[str] = []
    verbMoods: List[str] = []
    additionalFeatures: AdditionalFeatureSpec

class VowelHarmonySpec(BaseModel):
    isEnabled: bool
    inputs: Optional[Dict[str, List[str]]]


# Phonology Specification Model
class PhonologySpec(BaseModel):
    activeVowels: Optional[List[str]]
    activeConsonants: Optional[List[str]]
    vowelFrequencies: Optional[Dict[str, float]] = None
    consonantFrequencies: Optional[Dict[str, float]] = None
    mapping: Optional[Dict[str, str]] 
    allowedSyllables: Optional[List[str]] = ""
    transformationRules: Optional[str] = ""
    consonantClusters: Optional[List[str]] = None  
    vowelClusters: Optional[List[str]] = None 
    vowelHarmony: Optional["VowelHarmonySpec"] = None  

    @field_validator("consonantClusters", "vowelClusters", mode="before")
    @classmethod
    def split_comma_separated(cls, value):
        if isinstance(value, str):
            return value.split(",") 
        return value  




# Main Payload Model
class PayloadSpec(BaseModel):
    language: Optional[str]
    phonology: PhonologySpec
    grammar: GrammarSpec
