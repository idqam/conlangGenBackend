from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional

class PhonoTest(BaseModel):
    activeVowels: Optional[List[str]]
    activeConsonants: Optional[List[str] ]


# Additional Features Model
class AdditionalFeatureSpec(BaseModel):
    grammaticalGender: Optional[str] = ""
    evidentiality: Optional[str] = ""
    politeness: Optional[str] = ""
    negation: Optional[str] = ""
    pronounSystem: Optional[str] = ""

# Grammar Specification Model
class GrammarSpec(BaseModel):
    morphology:Optional[str] = ""
    wordOrder: Optional[str] = ""
    nounCases: Optional[str] = ""
    verbConjugation:Optional[str] = ""
    tenseAspectMood: Optional[str] = ""
    additionalFeatures: AdditionalFeatureSpec


class VowelHarmonySpec(BaseModel):
    isEnabled: bool
    inputs: Optional[Dict[str, List[str]]]


# Phonology Specification Model
class PhonologySpec(BaseModel):
    activeVowels: Optional[List[str]]
    activeConsonants: Optional[List[str]]
   
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
