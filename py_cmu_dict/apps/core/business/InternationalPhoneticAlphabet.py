import re

from typing import List


# https://en.m.wikipedia.org/wiki/ARPABET
# https://en.wikipedia.org/wiki/International_Phonetic_Alphabet
class InternationalPhoneticAlphabet:
    arpanet_phones = {
        "aa": "vowel",
        "ae": "vowel",
        "ah": "vowel",
        "ao": "vowel",
        "aw": "vowel",
        "ay": "vowel",
        "b": "stop",
        "ch": "affricate",
        "d": "stop",
        "dh": "fricative",
        "eh": "vowel",
        "er": "vowel",
        "ey": "vowel",
        "f": "fricative",
        "g": "stop",
        "hh": "aspirate",
        "ih": "vowel",
        "iy": "vowel",
        "jh": "affricate",
        "k": "stop",
        "l": "liquid",
        "m": "nasal",
        "n": "nasal",
        "ng": "nasal",
        "ow": "vowel",
        "oy": "vowel",
        "p": "stop",
        "r": "liquid",
        "s": "fricative",
        "sh": "fricative",
        "t": "stop",
        "th": "fricative",
        "uh": "vowel",
        "uw": "vowel",
        "v": "fricative",
        "w": "semivowel",
        "y": "semivowel",
        "z": "fricative",
        "zh": "fricative",
    }
    arpanet_hiatus = [["er", "iy"], ["iy", "ow"], ["uw", "ow"], ["iy", "ah"], ["iy", "ey"], ["uw", "eh"], ["er", "eh"]]
    arpanet_to_ipa = {
        "a": "ə",
        "ey": "eɪ",
        "aa": "ɑ",
        "ae": "æ",
        "ah": "ə",
        "ao": "ɔ",
        "aw": "aʊ",
        "ay": "aɪ",
        "ch": "ʧ",
        "dh": "ð",
        "eh": "ɛ",
        "er": "ər",
        "hh": "h",
        "ih": "ɪ",
        "jh": "ʤ",
        "ng": "ŋ",
        "ow": "oʊ",
        "oy": "ɔɪ",
        "sh": "ʃ",
        "th": "θ",
        "uh": "ʊ",
        "uw": "u",
        "zh": "ʒ",
        "iy": "i",
        "y": "j",
    }

    @classmethod
    def arpanet_syllable_count(cls, phonemes: List[str]) -> int:
        # Stress should be wipe out!
        cleaned_phonemes = [cls._erase_stress_from_arpanet_phoneme(phoneme) for phoneme in phonemes]
        # This will indicate how many syllable all the phonemes has
        nuclei_count = 0

        for index, current_phoneme in enumerate(cleaned_phonemes):
            previous_phoneme = cleaned_phonemes[index - 1]
            phone_type_previous_phoneme = cls.arpanet_phones[previous_phoneme]

            if cls.arpanet_phones[current_phoneme] == "vowel":
                if index > 0 and not phone_type_previous_phoneme == "vowel" or index == 0:
                    nuclei_count += 1
                elif [previous_phoneme, current_phoneme] in cls.arpanet_hiatus:
                    nuclei_count += 1

        return nuclei_count

    @staticmethod
    def _erase_stress_from_arpanet_phoneme(phoneme):
        return re.sub(r"\d", "", phoneme)
