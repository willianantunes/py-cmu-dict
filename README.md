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

## Running the project

Just issue the following command:

    docker-compose up remote-interpreter

You can access it through the address `http://localhost:8080/admin/`. Use `admin` for _username_ and _password_.

If you'd like to run without Docker, you can install the dependencies issuing `pipenv install`. After it's completed, you can enter `pipenv shell` and then type `./scripts/start-development.sh`. After the server is up, use the same address and credentials shown above.

## Running all the tests and evaluating lint

For the first one you can do:

    docker-compose up tests

For lint:

    docker-compose up lint

By the way, all the tests reports will be available in `tests-reports` folder. It will be created after tests execution. Check [start-tests.sh](scripts/start-tests.sh) to understand more. 
