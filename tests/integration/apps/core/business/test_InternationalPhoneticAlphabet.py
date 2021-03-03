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


def test_should_apply_stress_for_arpaned_phonemes_scenario_1():
    callable = InternationalPhoneticAlphabet.apply_ipa_stress_marks_to_arpanet_phoneme

    assert callable(["ah0"]) == ["ah"]
    assert callable(["ey1"]) == ["ey"]
    assert callable(["iy1", "ah0"]) == ["ˈiy", "ah"]
    assert callable(["aa1", "k", "er0"]) == ["ˈaa", "k", "er"]
    assert callable(["b", "iy1", "jh", "ey1"]) == ["ˈb", "iy", "ˈjh", "ey"]
    assert callable(["s", "ah1", "m", "th", "ih0", "ng"]) == ["ˈs", "ah", "m", "th", "ih", "ng"]
    assert callable(["ey1", "f", "ao1", "r", "t", "uw1", "w", "ah1", "n", "t", "uw1", "ey1", "t"]) == [
        "ˈey",
        "ˈf",
        "ao",
        "r",
        "ˈt",
        "uw",
        "ˈw",
        "ah",
        "n",
        "ˈt",
        "uw",
        "ˈey",
        "t",
    ]
    assert callable(["th", "iy2", "er0", "eh1", "t", "ih0", "k", "ah0", "l", "iy0"]) == [
        "ˌth",
        "iy",
        "er",
        "ˈeh",
        "t",
        "ih",
        "k",
        "ah",
        "l",
        "iy",
    ]


def test_should_transform_arpanet_to_ipa_scenario_1():
    arpanet_1 = ["ey1", "f", "ao1", "r", "t", "uw1", "w", "ah1", "n", "t", "uw1", "ey1", "t"]
    ipa_1 = ["ˈeɪ", "ˈf", "ɔ", "ɹ", "ˈt", "u", "ˈw", "ə", "n", "ˈt", "u", "ˈeɪ", "t"]

    assert InternationalPhoneticAlphabet.ipa_format_from_arpanet(arpanet_1) == ipa_1

    arpanet_2 = ["s", "ah1", "m", "th", "ih0", "ng"]
    ipa_2 = ["ˈs", "ə", "m", "θ", "ɪ", "ŋ"]
    assert InternationalPhoneticAlphabet.ipa_format_from_arpanet(arpanet_2) == ipa_2
