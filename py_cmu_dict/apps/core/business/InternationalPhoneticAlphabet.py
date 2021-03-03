import re

from typing import List

# https://en.m.wikipedia.org/wiki/ARPABET
# https://en.wikipedia.org/wiki/International_Phonetic_Alphabet
# http://english.glendale.cc.ca.us/phonics.rules.html
from py_cmu_dict.apps.core.business.exceps import MoreThanOneARPANETStressMarkException


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
    arpanet_hiatus = [
        ["er", "iy"],
        ["iy", "ow"],
        ["uw", "ow"],
        ["iy", "ah"],
        ["iy", "ey"],
        ["uw", "eh"],
        ["er", "eh"],
    ]
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
    arpanet_stress_mark_to_ipa = {
        "1": "ˈ",
        "2": "ˌ",
    }
    regex_to_clean_arpanet_and_ipa_stress_mark = r"[\dˈˌ]"

    @classmethod
    def arpanet_syllable_count(cls, phonemes: List[str]) -> int:
        # Stress should be wipe out!
        cleaned_phonemes = [cls._erase_stress_from_arpanet_phoneme(phoneme) for phoneme in phonemes]
        # This will indicate how many syllable all the phonemes has
        nuclei_count = 0

        for index, current_phoneme in enumerate(cleaned_phonemes):
            if cls.arpanet_phones[current_phoneme] == "vowel":
                first_iteration = index == 0

                if first_iteration:
                    nuclei_count += 1
                else:
                    previous_phoneme = cleaned_phonemes[index - 1]
                    previous_phoneme_type = cls.arpanet_phones[previous_phoneme]
                    previous_phoneme_type_is_not_vowel = not previous_phoneme_type == "vowel"

                    if previous_phoneme_type_is_not_vowel:
                        nuclei_count += 1
                    elif [previous_phoneme, current_phoneme] in cls.arpanet_hiatus:
                        nuclei_count += 1

        return nuclei_count

    @classmethod
    def apply_ipa_stress_marks_to_arpanet_phoneme(cls, phonemes: List[str]) -> List[str]:
        clusters = ["sp", "st", "sk", "fr", "fl"]
        # stop searching for where stress starts if these are encountered
        stop_set = ["nasal", "fricative", "vowel"]

        number_of_syllables = cls.arpanet_syllable_count(phonemes)
        eligible_to_apply_ipa_stress = number_of_syllables > 1
        if not eligible_to_apply_ipa_stress:
            return [cls._erase_stress_from_arpanet_phoneme(phoneme) for phoneme in phonemes]
        else:
            updated_phonemes = []
            for phoneme in phonemes:
                phoneme_last_char = phoneme[-1]
                phoneme_eligible_to_be_evaluated = phoneme_last_char in cls.arpanet_stress_mark_to_ipa.keys()
                if not phoneme_eligible_to_be_evaluated:
                    updated_phonemes.append(cls._erase_stress_from_arpanet_phoneme(phoneme))
                else:
                    # Extracting symbol
                    all_matches = re.findall(r"\d", phoneme)
                    if len(all_matches) > 1:
                        raise MoreThanOneARPANETStressMarkException
                    arpanet_stress_mark = all_matches[0]
                    ipa_symbol = cls.arpanet_stress_mark_to_ipa[arpanet_stress_mark]
                    # Given the array is empty, we can do the simple work
                    if not updated_phonemes:
                        cleaned_phoneme = cls._erase_stress_from_arpanet_phoneme(phoneme)
                        new_phoneme = f"{ipa_symbol}{cleaned_phoneme}"
                        updated_phonemes.append(new_phoneme)
                    else:
                        placed, hiatus = False, False
                        # Inverting to make the analysis easier
                        updated_phonemes = updated_phonemes[::-1]
                        # fmt: off
                        for index, updated_phoneme in enumerate(updated_phonemes):
                            first_iteration = index == 0
                            cleaned_updated_phoneme = re.sub(cls.regex_to_clean_arpanet_and_ipa_stress_mark, "", updated_phoneme)
                            cleaned_updated_phoneme_type = cls.arpanet_phones[cleaned_updated_phoneme]

                            if cleaned_updated_phoneme_type in stop_set:
                                if cleaned_updated_phoneme_type == "vowel":
                                    hiatus = True
                                    cleaned_phoneme = cls._erase_stress_from_arpanet_phoneme(phoneme)
                                    new_phoneme = f"{ipa_symbol}{cleaned_phoneme}"
                                    updated_phonemes.append(new_phoneme)
                                else:
                                    updated_phonemes[index] = ipa_symbol + updated_phonemes[index]
                            else:
                                previous_updated_phoneme = updated_phonemes[index - 1]
                                cleaned_previous_updated_phoneme = re.sub(cls.regex_to_clean_arpanet_and_ipa_stress_mark, "", previous_updated_phoneme)
                                cleaned_previous_updated_phoneme_type = cls.arpanet_phones[cleaned_previous_updated_phoneme]
                                first_eligibility = not first_iteration and cleaned_previous_updated_phoneme_type == "stop"
                                second_eligibility = cleaned_updated_phoneme in ["er", "w", "jh"]
                                if first_eligibility or second_eligibility:
                                    conjunction = f"{cleaned_updated_phoneme}{cleaned_previous_updated_phoneme}"
                                    if conjunction in clusters:
                                        updated_phonemes[index] = ipa_symbol + updated_phonemes[index]
                                    elif not cleaned_previous_updated_phoneme_type == "vowel":
                                        updated_phonemes[index - 1] = ipa_symbol + updated_phonemes[index - 1]
                                placed = True
                                break
                        # fmt: on
                        if not placed:
                            index_to_place_refreshed_phoneme = len(updated_phonemes) - 1
                            refreshed_phoneme = ipa_symbol + updated_phonemes[index_to_place_refreshed_phoneme]
                            updated_phonemes[index_to_place_refreshed_phoneme] = refreshed_phoneme
                        # Normal order
                        updated_phonemes = updated_phonemes[::-1]
                        if not hiatus:
                            cleaned_phoneme = cls._erase_stress_from_arpanet_phoneme(phoneme)
                            updated_phonemes.append(cleaned_phoneme)
            return updated_phonemes

    @staticmethod
    def _erase_stress_from_arpanet_phoneme(phoneme):
        return re.sub(r"\d", "", phoneme)
