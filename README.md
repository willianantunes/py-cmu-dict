# PY-CMU-DICT

I really wanted to know more about [CMU Pronouncing Dictionary](https://en.wikipedia.org/wiki/CMU_Pronouncing_Dictionary), that is why I created this project. Here you'll understand how to handle the dictionary, how to deal with its phoneme scheme and how to translate it to IPA format. Main classes/modules that you should check:

- [CMUDatabaseHandler](py_cmu_dict/apps/core/business/CMUDatabaseHandler.py)
- [InternationalPhoneticAlphabet](py_cmu_dict/apps/core/business/CMUDatabaseHandler.py)
- [word_classifier](py_cmu_dict/apps/core/business/word_classifier.py)

Each one has a specific test counterpart that verifies whether the logic is satisfied or not:

- [test_CMUDatabaseHandler](tests/integration/apps/core/business/test_CMUDatabaseHandler.py)
- [test_InternationalPhoneticAlphabet](tests/integration/apps/core/business/test_InternationalPhoneticAlphabet.py)
- [test_word_classifier](tests/integration/apps/core/business/test_word_classifier.py)

## Important projects out there

It's important that you know that this playground would not be possible without the following projects:

- [mphilli/English-to-IPA](https://github.com/mphilli/English-to-IPA)
- [repp/big-phoney](https://github.com/repp/big-phoney)
- [cmusphinx/cmudict-tools](https://github.com/cmusphinx/cmudict-tools)
- [JoseLlarena/Britfone](https://github.com/JoseLlarena/Britfone)

The first one was indeed the game changer here.

## How to run the project

TODO.

## Running the tests

TODO.
