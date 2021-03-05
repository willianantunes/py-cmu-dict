#!/usr/bin/env bash

python manage.py makemigrations
python manage.py migrate
WHERE_CMU_DATABASE_FILE_IS=$(pwd)/tests/resources/cmudict-0.7b.txt
python manage.py seed --create-super-user --cmu-file-location "$WHERE_CMU_DATABASE_FILE_IS"

python manage.py runserver 0.0.0.0:8000
