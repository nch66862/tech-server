# Takes data from the database and creates fixture data for each table and puts the files in the root directory
# run sh ./fetch_data.sh from the terminal in the root directory
# it puts the .json files in the fetched_fixtures directory

python3 manage.py dumpdata auth.user --indent 4 > ./fetched_fixtures/users.json
python3 manage.py dumpdata authtoken.token --indent 4 > ./fetched_fixtures/tokens.json
python3 manage.py dumpdata priorityapi.affirmation --indent 4 > ./fetched_fixtures/affirmations.json