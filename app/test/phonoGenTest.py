import pytest
from app.models.schemas import PhonologySpec, VowelHarmonySpec
from app.services.phonoGen import generate_valid_words, map_to_user_defined_form

def test_generate_valid_words():
    phonology_spec = PhonologySpec(
        activeVowels=["ɑ", "ɛ", "i", "o", "u", "e", "æ", "ʊ", "ɪ", "ʌ"],
        activeConsonants=[
            "p", "t", "k", "s", "m", "n", "b", "d", "g", "f", "v", "θ", "ð", "ʃ", "ʒ", "ʧ", "ʤ", 
            "l", "r", "j", "w", "h", "ɡ", "ŋ", "ɾ"
        ],
        mapping={  # IPA to user-defined mapping
            "ɑ": "a", "ɛ": "é", "i": "i", "o": "o", "u": "u",
            "e": "é", "æ": "ä", "ʊ": "û", "ɪ": "ï", "ʌ": "ô",
            "p": "p", "t": "t", "k": "k", "s": "s", "m": "m", "n": "n",
            "b": "b", "d": "d", "g": "g", "f": "f", "v": "v", "θ": "th", "ð": "dh",
            "ʃ": "sh", "ʒ": "zh", "ʧ": "ch", "ʤ": "j", "l": "l", "r": "r", "j": "y", "w": "w",
            "h": "h", "ɡ": "g", "ŋ": "ng", "ɾ": "r"
        },
        allowedSyllables=["CVC", "CV", "VC", "V", "CCV", "CCVC", "VCC", "CVCV", "CVCC", "CVVC"],
        transformationRules=r"[θ > t / _C] [ð > d / V_V] [ʃ > s / #_] [ʒ > zh / _V] [ʧ > ch / _#] [ʤ > j / V_]",
        consonantClusters=["st", "pr", "kt", "fl", "gr", "skr", "sp", "tr", "bl", "dr"],
        vowelClusters=["ai", "oi", "ea", "ou", "ui", "ie", "ei", "oa"],
        vowelHarmony=VowelHarmonySpec(
            isEnabled=True,
            inputs={"front": ["i", "e", "ɛ", "æ", "ɪ"], "back": ["o", "u", "ʊ", "ʌ"], "neutral": ["ɑ"]}
        )
    )

    generated_words = generate_valid_words(phonology_spec, 100)
    assert len(generated_words) > 0, "No words were generated!"

    mapped_words = map_to_user_defined_form(generated_words, phonology_spec)
    assert all(word in mapped_words for word in generated_words), "Not all IPA words were mapped!"

    #print("Generated IPA Words:", generated_words)
    print("Mapped Words:", mapped_words.values())

test_generate_valid_words()