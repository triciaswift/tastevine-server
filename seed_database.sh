#!/bin/bash

rm db.sqlite3
rm -rf ./tastevineapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations tastevineapi
python3 manage.py migrate tastevineapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata grocerycategories
python3 manage.py loaddata ingredients
python3 manage.py loaddata categories
python3 manage.py loaddata recipes
python3 manage.py loaddata recipecategories
python3 manage.py loaddata recipeingredients
python3 manage.py loaddata favorites
python3 manage.py loaddata notes
python3 manage.py loaddata grocerylists
python3 manage.py loaddata grocerylistitems