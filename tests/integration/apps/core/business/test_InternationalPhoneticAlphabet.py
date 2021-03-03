from py_cmu_dict.apps.core.business.InternationalPhoneticAlphabet import InternationalPhoneticAlphabet


def test_should_count_syllables_for_arpanet_phonemes_scenario_1():
    phonemes_for_word_something = ["s", "ah1", "m", "th", "ih0", "ng"]
    number_of_syllables = InternationalPhoneticAlphabet.arpanet_syllable_count(phonemes_for_word_something)

    assert number_of_syllables == 2


def test_should_count_syllables_for_arpanet_phonemes_scenario_2():
    phonemes_for_word_solicitation = ["s", "ah0", "l", "ih2", "s", "ih0", "t", "ey1", "sh", "ah0", "n"]
    number_of_syllables = InternationalPhoneticAlphabet.arpanet_syllable_count(phonemes_for_word_solicitation)

    assert number_of_syllables == 5


def test_should_count_syllables_for_arpanet_phonemes_scenario_3():
    phonemes_for_word_sold = ["s", "ow1", "l", "d"]
    number_of_syllables = InternationalPhoneticAlphabet.arpanet_syllable_count(phonemes_for_word_sold)

    assert number_of_syllables == 1
