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


def test_should_count_syllables_for_arpanet_phonemes_scenario_4():
    phonemes_for_word_caramel = ["k", "eh1", "r", "ah0", "m", "ah0", "l"]
    number_of_syllables = InternationalPhoneticAlphabet.arpanet_syllable_count(phonemes_for_word_caramel)

    assert number_of_syllables == 3


def test_should_count_syllables_for_arpanet_phonemes_scenario_5():
    # The word "came" has 2 vowels, but the "e" is silent, leaving one vowel sound and 1 syllable
    phonemes_for_word_came = ["k", "ey1", "m"]
    number_of_syllables = InternationalPhoneticAlphabet.arpanet_syllable_count(phonemes_for_word_came)

    assert number_of_syllables == 1


def test_should_count_syllables_for_arpanet_phonemes_scenario_6():
    # The word "outside" has 4 vowels, but the "e" is silent and the "ou" is a diphthong which counts as only one sound,
    # so this word has only two vowels sounds and therefore, 2 syllables.
    phonemes_for_word_outside = ["aw1", "t", "s", "ay1", "d"]
    number_of_syllables = InternationalPhoneticAlphabet.arpanet_syllable_count(phonemes_for_word_outside)

    assert number_of_syllables == 2
