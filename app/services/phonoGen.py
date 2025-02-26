import re
import random
from typing import List, Dict, Optional

class VowelHarmonySpec:
    def __init__(self, isEnabled: bool, inputs: Dict[str, List[str]]):
        self.isEnabled = isEnabled
        self.inputs = inputs

class PhonologySpec:
    def __init__(self, activeVowels: List[str], activeConsonants: List[str],
                 vowelFrequencies: Optional[Dict[str, float]],
                 consonantFrequencies: Optional[Dict[str, float]],
                 mapping: Dict[str, str],
                 allowedSyllables: List[str],
                 transformationRules: str,
                 consonantClusters: List[str],
                 vowelClusters: List[str],
                 vowelHarmony: Optional[VowelHarmonySpec]):
        self.activeVowels = activeVowels
        self.activeConsonants = activeConsonants
        
        self.vowelFrequencies = self._normalize_frequencies(
            vowelFrequencies or {v: random.random() for v in activeVowels}
        )
        self.consonantFrequencies = self._normalize_frequencies(
            consonantFrequencies or {c: random.random() for c in activeConsonants}
        )
        
        self.mapping = mapping
        self.allowedSyllables = allowedSyllables if allowedSyllables else ["CV", "CVC", "VC"]
        self.transformationRules = transformationRules if transformationRules else "[x>x]"
        self.consonantClusters = consonantClusters if consonantClusters else ["tr", "dr", "pl", "st"]
        self.vowelClusters = vowelClusters if vowelClusters else ["ai", "ei", "ou", "au"]
        self.vowelHarmony = vowelHarmony

    def _normalize_frequencies(self, freq_dict: Dict[str, float]) -> Dict[str, float]:
        total = sum(freq_dict.values())
        return {phoneme: freq / total for phoneme, freq in freq_dict.items()}

def apply_transformation_rules(word: str, transformation_rules: str) -> str:
   
    if not transformation_rules:
        return word

    transformations = re.findall(r'\[(.*?)\]', transformation_rules)
    for rule in transformations:
        parts = rule.split('>')
        if len(parts) < 2:
            continue

        from_part = parts[0].strip()
        to_part = parts[1].split('/')[0].strip()
        conditions = re.search(r'/ (.+)', rule)
        if conditions:
            condition = conditions.group(1).strip()
            if ' \ ' in condition:
                match = re.search(r'(.+?) \ (.+)', condition)
                if match:
                    before, after = match.groups()
                    word = re.sub(r'(?<=%s)%s' % (before, from_part), to_part, word)
            elif ' / ' in condition:
                match = re.search(r'(.+?) / (.+)', condition)
                if match:
                    before, after = match.groups()
                    word = re.sub(r'%s(?=%s)' % (from_part, after), to_part, word)
            elif '^' in condition:
                match = re.search(r'(.+?) \^ (.+)', condition)
                if match:
                    phoneme, cond = match.groups()
                    if phoneme in word:
                        word = word.replace(phoneme, to_part)
        else:
            word = word.replace(from_part, to_part)
    return word

def enforce_cluster_rules(word: str, active_vowels: List[str], active_consonants: List[str],
                          allowed_consonant_clusters: List[str],
                          allowed_vowel_clusters: List[str]) -> bool:
    """
    Checks that any sequence of 2 or more consecutive IPA vowels or consonants in `word`
    appears in the allowed cluster lists.
    """
    cons_pattern = f"[{re.escape(''.join(active_consonants))}]" + "{2,}"
    vowel_pattern = f"[{re.escape(''.join(active_vowels))}]" + "{2,}"
    
    found_cons_clusters = re.findall(cons_pattern, word)
    for cluster in found_cons_clusters:
        if cluster not in allowed_consonant_clusters:
            return False

    found_vowel_clusters = re.findall(vowel_pattern, word)
    for cluster in found_vowel_clusters:
        if cluster not in allowed_vowel_clusters:
            return False

    return True

def apply_vowel_harmony(word: str, vowel_harmony: Optional[VowelHarmonySpec]) -> str:
    """
    Adjusts vowels in the IPA word based on vowel harmony rules.
    """
    if not vowel_harmony or not vowel_harmony.isEnabled:
        return word

    front_vowels = set(vowel_harmony.inputs.get("front", []))
    back_vowels = set(vowel_harmony.inputs.get("back", []))
    neutral_vowels = set(vowel_harmony.inputs.get("neutral", []))
    
    word_vowels = [char for char in word if char in front_vowels or char in back_vowels or char in neutral_vowels]
    if not word_vowels:
        return word

    front_count = sum(1 for v in word_vowels if v in front_vowels)
    back_count = sum(1 for v in word_vowels if v in back_vowels)
    
    if front_count > back_count:
        dominant_class = front_vowels
    elif back_count > front_count:
        dominant_class = back_vowels
    else:
        dominant_class = neutral_vowels

    new_word = "".join(
        random.choice(list(dominant_class)) if char in front_vowels or char in back_vowels else char
        for char in word
    )
    return new_word

def generate_syllable(structure: str, phonology: PhonologySpec) -> str:
    """
    Generates a syllable following the given structure.
    'C' selects an IPA consonant based on frequency;
    'V' selects an IPA vowel based on frequency.
    """
    syllable = ""
    for char in structure:
        if char == "C":
            syllable += random.choices(
                phonology.activeConsonants,
                weights=[phonology.consonantFrequencies[c] for c in phonology.activeConsonants]
            )[0]
        elif char == "V":
            syllable += random.choices(
                phonology.activeVowels,
                weights=[phonology.vowelFrequencies[v] for v in phonology.activeVowels]
            )[0]
    return syllable

def generate_valid_words(phonology: PhonologySpec, wordMax: int) -> List[str]:
    """
    Generates words that:
      - Follow allowed syllable structures,
      - Apply transformation rules,
      - Contain only allowed IPA clusters (vowel and consonant),
      - And apply vowel harmony (if enabled).
    """
    w = set()
    while len(w) < wordMax:
        syllable_structure = random.choice(phonology.allowedSyllables)
        base_word = generate_syllable(syllable_structure, phonology)
        transformed_word = apply_transformation_rules(base_word, phonology.transformationRules)
        
        if not enforce_cluster_rules(
            transformed_word,
            phonology.activeVowels,
            phonology.activeConsonants,
            phonology.consonantClusters,
            phonology.vowelClusters
        ):
            continue 
        
        final_word = apply_vowel_harmony(transformed_word, phonology.vowelHarmony)
        w.add(final_word)
    words = list(w)
    return words

def map_to_user_defined_form(ipa_words: List[str], phonology: PhonologySpec) -> List[str]:
    """
    Converts IPA words into user-defined symbols based on the provided mapping.
    Transformation occurs after all IPA logic (including allowed cluster checks) is complete.
    """
    return [
        "".join(phonology.mapping.get(char, char) for char in ipa_word)
        for ipa_word in ipa_words
    ]
