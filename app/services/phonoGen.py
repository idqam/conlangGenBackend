import re
import random
from typing import List, Dict, Optional

class VowelHarmonySpec:
    def __init__(self, isEnabled: bool, inputs: Dict[str, List[str]]):
        self.isEnabled = isEnabled
        self.inputs = inputs

class PhonologySpec:
    def __init__(self, activeVowels: List[str], activeConsonants: List[str], 
                 mapping: Dict[str, str], allowedSyllables: List[str], 
                 transformationRules: str, consonantClusters: List[str], 
                 vowelClusters: List[str], vowelHarmony: Optional[VowelHarmonySpec]):
        self.activeVowels = activeVowels
        self.activeConsonants = activeConsonants
        self.mapping = mapping
        
        self.allowedSyllables = allowedSyllables if allowedSyllables else ["CV", "CVC", "VC"]
        self.transformationRules = transformationRules if transformationRules else "[x>x]"
        self.consonantClusters = consonantClusters if consonantClusters else ["tr", "dr", "pl", "st"]
        self.vowelClusters = vowelClusters if vowelClusters else ["ai", "ei", "ou", "au"]
        
        self.vowelHarmony = vowelHarmony


def apply_transformation_rules(word: str, transformation_rules: str) -> str:
    """
    Applies transformation rules defined in the rule syntax.
    """
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
                # X > Y \ O (After)
                match = re.search(r'(.+?) \ (.+)', condition)
                if match:
                    before, after = match.groups()
                    word = re.sub(r'(?<=%s)%s' % (before, from_part), to_part, word)

            elif ' / ' in condition:
                # X > Y / O (Before)
                match = re.search(r'(.+?) / (.+)', condition)
                if match:
                    before, after = match.groups()
                    word = re.sub(r'%s(?=%s)' % (from_part, after), to_part, word)

            elif '^' in condition:
                # Conditional Replacement
                match = re.search(r'(.+?) \^ (.+)', condition)
                if match:
                    phoneme, cond = match.groups()
                    if phoneme in word:
                        word = word.replace(phoneme, to_part)
        else:
            word = word.replace(from_part, to_part)

    return word


def enforce_cluster_rules(word: str, consonant_clusters: List[str], vowel_clusters: List[str]) -> bool:
    """
    Ensures the word only contains valid consonant and vowel clusters.
    - Words that contain clusters must use only the allowed ones.
    - Words that don't contain any clusters are still valid.
    """
    
    found_consonant_clusters = re.findall(r"[bcdfghjklmnpqrstvwxyz]{2,}", word)

    if found_consonant_clusters:
        for cluster in found_consonant_clusters:
            if cluster not in consonant_clusters:
                return False  

    found_vowel_clusters = re.findall(r"[aeiou]{2,}", word)

    if found_vowel_clusters:
        for cluster in found_vowel_clusters:
            if cluster not in vowel_clusters:
                return False  
    return True  


def apply_vowel_harmony(word: str, vowel_harmony: VowelHarmonySpec) -> str:
    """
    Adjusts vowels in the word based on vowel harmony rules.
    """
    if not vowel_harmony.isEnabled:
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


def generate_valid_words(phonology: PhonologySpec, wordMax: int) -> List[str]:
    """
    Generates words that:
    - Follow allowed syllable structures.
    - Apply transformation rules.
    - Only contain valid consonant and vowel clusters.
    - Apply vowel harmony (if enabled).
    """
    words = []

    def generate_syllable(structure: str, phonology: PhonologySpec) -> str:
        """ Generates a syllable following the given structure. """
        syllable = ""
        for char in structure:
            if char == "C":
                syllable += random.choice(phonology.activeConsonants)
            elif char == "V":
                syllable += random.choice(phonology.activeVowels)
        return syllable

    for _ in range(wordMax): 
        syllable_structure = random.choice(phonology.allowedSyllables)
        base_word = generate_syllable(syllable_structure, phonology)

        transformed_word = apply_transformation_rules(base_word, phonology.transformationRules)

        if not enforce_cluster_rules(transformed_word, phonology.consonantClusters, phonology.vowelClusters):
            continue  # Reject word and generate a new one

        final_word = apply_vowel_harmony(transformed_word, phonology.vowelHarmony)

        words.append(final_word)

    return words

def map_to_user_defined_form(ipa_words: List[str], phonology: PhonologySpec) -> Dict[str, str]:
    """
    Converts IPA words to their user-defined forms based on phonology mapping.
    
    Args:
        ipa_words (List[str]): A list of words in IPA.
        phonology (PhonologySpec): The phonology configuration containing the mapping.

    Returns:
        Dict[str, str]: A dictionary mapping IPA words to user-defined words.
    """
    mapped_words = {}
    mapping = phonology.mapping

    convertedWords = ["".join(mapping[char] if char in mapping else char for char in ipa_word) for ipa_word in ipa_words]

    return convertedWords
