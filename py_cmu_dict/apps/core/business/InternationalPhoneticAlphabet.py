import re

from collections import deque
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
        "f": "f",
        "g": "ɡ",
        "hh": "h",
        "ih": "ɪ",
        "jh": "ʤ",
        "n": "n",
        "ng": "ŋ",
        "ow": "oʊ",
        "oy": "ɔɪ",
        "r": "ɹ",
        "sh": "ʃ",
        "t": "t",
        "th": "θ",
        "uh": "ʊ",
        "uw": "u",
        "w": "w",
        "zh": "ʒ",
        "iy": "i",
        "s": "s",
        "m": "m",
        "y": "j",
    }
    arpanet_stress_mark_to_ipa = {
        "1": "ˈ",
        "2": "ˌ",
    }
    regex_to_clean_arpanet_and_ipa_stress_mark = (
        fr"[\d{arpanet_stress_mark_to_ipa['1']}{arpanet_stress_mark_to_ipa['2']}]"
    )
    regex_to_capture_ipa_stress_mark = fr"([\{arpanet_stress_mark_to_ipa['1']}\{arpanet_stress_mark_to_ipa['2']}])"

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
        # Stop searching for where stress starts if these are encountered
        stop_set = ["nasal", "fricative", "vowel"]

        number_of_syllables = cls.arpanet_syllable_count(phonemes)
        eligible_to_apply_ipa_stress = number_of_syllables > 1
        if not eligible_to_apply_ipa_stress:
            return [cls._erase_stress_from_arpanet_phoneme(phoneme) for phoneme in phonemes]
        else:
            updated_phonemes = deque()
            for phoneme in phonemes:
                phoneme_last_char = phoneme[-1]
                phoneme_eligible_to_be_evaluated = phoneme_last_char in cls.arpanet_stress_mark_to_ipa.keys()
                if not phoneme_eligible_to_be_evaluated:
                    updated_phonemes.append(cls._erase_stress_from_arpanet_phoneme(phoneme))
                else:
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
                        updated_phonemes.reverse()
                        for index, updated_phoneme in enumerate(updated_phonemes):
                            not_first_iteration = index > 0
                            # Deal with updated_phoneme
                            cleaned_updated_phoneme = cls._clean_all_stress_marks(updated_phoneme)
                            cleaned_updated_phoneme_type = cls.arpanet_phones[cleaned_updated_phoneme]
                            # Deal with previous phoneme
                            previous_updated_phoneme = updated_phonemes[index - 1]
                            cleaned_previous_updated_phoneme = cls._clean_all_stress_marks(previous_updated_phoneme)
                            cleaned_previous_updated_phoneme_type = cls.arpanet_phones[cleaned_previous_updated_phoneme]
                            # Eligibility rules
                            first_eligibility = cleaned_updated_phoneme_type in stop_set
                            second_eligibility = not_first_iteration and cleaned_previous_updated_phoneme_type == "stop"
                            third_eligibility = cleaned_updated_phoneme in ["er", "w"]

                            if first_eligibility or second_eligibility or third_eligibility:
                                conjunction = f"{cleaned_updated_phoneme}{cleaned_previous_updated_phoneme}"
                                if conjunction in clusters:
                                    updated_phonemes[index] = ipa_symbol + updated_phonemes[index]
                                elif not cleaned_previous_updated_phoneme_type == "vowel" and not_first_iteration:
                                    updated_phonemes[index - 1] = ipa_symbol + updated_phonemes[index - 1]
                                elif cleaned_updated_phoneme_type == "vowel":
                                    hiatus = True
                                    cleaned_phoneme = cls._erase_stress_from_arpanet_phoneme(phoneme)
                                    new_phoneme = f"{ipa_symbol}{cleaned_phoneme}"
                                    updated_phonemes.appendleft(new_phoneme)
                                else:
                                    updated_phonemes[index] = ipa_symbol + updated_phonemes[index]
                                placed = True
                                break
                        if not placed:
                            index_to_place_refreshed_phoneme = len(updated_phonemes) - 1
                            refreshed_phoneme = ipa_symbol + updated_phonemes[index_to_place_refreshed_phoneme]
                            updated_phonemes[index_to_place_refreshed_phoneme] = refreshed_phoneme
                        # Normal order
                        updated_phonemes.reverse()
                        if not hiatus:
                            cleaned_phoneme = cls._erase_stress_from_arpanet_phoneme(phoneme)
                            updated_phonemes.append(cleaned_phoneme)
            return list(updated_phonemes)

    @classmethod
    def ipa_format_from_arpanet(cls, phonemes: List[str]) -> List[str]:
        swap_list = [("ˈər", "əˈr"), ("ˈie", "iˈe")]
        phonemes_as_ipa_symbols = []
        refreshed_phonemes = cls.apply_ipa_stress_marks_to_arpanet_phoneme(phonemes)

        for index, phoneme in enumerate(refreshed_phonemes):
            matches = list(re.finditer(cls.regex_to_capture_ipa_stress_mark, phoneme))
            if not matches:
                ipa_version = cls.arpanet_to_ipa[phoneme]
                phonemes_as_ipa_symbols.append(ipa_version)
            else:
                match = matches[0]
                mark_that_was_matched = match.group()
                phoneme_without_stress = phoneme[match.end() :]
                ipa_version = cls.arpanet_to_ipa[phoneme_without_stress]
                final_ipa_version = f"{mark_that_was_matched}{ipa_version}"
                phonemes_as_ipa_symbols.append(final_ipa_version)
        for to_compare, to_swap in swap_list:
            if not phonemes_as_ipa_symbols[0].startswith(to_compare):
                phonemes_as_ipa_symbols[0] = phonemes_as_ipa_symbols[0].replace(to_compare, to_swap)

        return phonemes_as_ipa_symbols

    @staticmethod
    def _erase_stress_from_arpanet_phoneme(phoneme):
        return re.sub(r"\d", "", phoneme)

    @classmethod
    def _clean_all_stress_marks(cls, phoneme):
        return re.sub(cls.regex_to_clean_arpanet_and_ipa_stress_mark, "", phoneme)
