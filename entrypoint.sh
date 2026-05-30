#!/bin/sh
set -e

python manage.py migrate --noinput

if [ "${SYNC_JOKES_FROM_FIXTURE:-true}" = "true" ] && [ -f "${JOKES_FIXTURE:-fixtures/jokes.json}" ]; then
  python manage.py sync_jokes_fixture --fixture "${JOKES_FIXTURE:-fixtures/jokes.json}"
fi

python manage.py collectstatic --noinput

exec gunicorn dad_jokes_project.wsgi:application \
  --bind "0.0.0.0:${PORT:-80}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --timeout "${WEB_TIMEOUT:-60}"
