#!/bin/sh
set -e

mkdir -p fixtures
poetry run python manage.py dumpdata jokes.Joke --indent 2 --output fixtures/jokes.json
poetry run python manage.py sync_jokes_fixture --fixture fixtures/jokes.json --dry-run
