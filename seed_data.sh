#!/bin/bash
# type this (sh ./seed_data.sh) into terminal to run

rm db.sqlite3
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens