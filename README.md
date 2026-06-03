# Dad Jokes

A minimal Django app for testing deployment. The home page displays one random dad joke prompt from the database, reveals the punchline when present, and links back to itself to show another joke.

Repository: `git@github.com:delger/dad-jokes.git`

## Requirements

- Python 3.13 or newer
- Poetry

## Local Setup

Install dependencies:

```bash
poetry install
```

This project uses Poetry for dependency management. The in-project virtual environment is configured in `poetry.toml`, so Poetry will create/use `.venv/`.

## Database

Local development uses Postgres by default:

```bash
postgres://donaldelger@localhost:5432/dad_jokes
```

If the database does not exist yet, create it:

```bash
createdb -h localhost -p 5432 dad_jokes
```

Create and apply local migrations:

```bash
poetry run python manage.py migrate
```

The `jokes` app includes a data migration that inserts three starter jokes.

## Production Database

Production uses Postgres through `DATABASE_URL`. Create a Postgres database in CapRover, then set `DATABASE_URL` for the app:

```bash
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME
```

Run migrations after `DATABASE_URL` is configured:

```bash
poetry run python manage.py migrate
```

## Admin

Create an admin user:

```bash
poetry run python manage.py createsuperuser
```

Then visit `/admin/` and sign in to manage jokes.

## Run Locally

```bash
poetry run python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

## Tests

Run the test suite:

```bash
poetry run python manage.py test
```

Tests cover the home page, admin redirect, model behavior, production static-file settings, and joke fixture sync automation.

## Static Files

Collect static assets for production:

```bash
poetry run python manage.py collectstatic --noinput
```

WhiteNoise is configured to serve collected static files.

## Docker

Build the image locally:

```bash
docker build -t dad-jokes .
```

Run the container locally:

```bash
docker run --rm -p 8000:80 \
  -e SECRET_KEY=dev-test-secret \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  -e DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME \
  dad-jokes
```

The container runs migrations, syncs jokes from `fixtures/jokes.json` when present, collects static files, and starts Gunicorn on port `80`.

## Production Environment Variables

Set these environment variables in production:

```bash
SECRET_KEY=replace-with-a-secure-secret
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME
```

`ALLOWED_HOSTS` is a comma-separated list. Production should set `DATABASE_URL` to the production Postgres database.

## Joke Data Source of Truth

The local Postgres database is the source of truth for joke data. Production receives a published snapshot from `fixtures/jokes.json`.

After adding, editing, or deleting jokes locally, export the current joke data:

```bash
./scripts/export-jokes.sh
```

This writes `fixtures/jokes.json` from the local database and runs a dry-run sync check.

During Docker/container startup, `entrypoint.sh` runs migrations and then syncs production jokes from `fixtures/jokes.json` when the fixture exists. The sync creates missing jokes and deletes production jokes that are not in the fixture, so production matches the local source-of-truth snapshot.

To disable automatic fixture sync for a deployment:

```bash
SYNC_JOKES_FROM_FIXTURE=false
```

To use a different fixture path:

```bash
JOKES_FIXTURE=fixtures/other-jokes.json
```

## Deployment Path

1. Add or edit jokes locally.
2. Export joke data with `./scripts/export-jokes.sh`.
3. Build locally.
4. Dockerize the app.
5. Deploy with CapRover.
6. Attach the domain.
7. Enable HTTPS.

## Deployment Checklist

- Confirm the app runs locally with `poetry run python manage.py runserver`.
- Export local joke data with `./scripts/export-jokes.sh`.
- Build and test the Docker image locally.
- Create or attach a Postgres database in CapRover.
- Set production environment variables in CapRover: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and `DATABASE_URL`.
- Deploy the app through CapRover using `captain-definition`.
- Confirm the container startup runs migrations, syncs jokes from `fixtures/jokes.json`, and collects static files.
- Create a superuser if admin access is needed.
- Attach the custom domain in CapRover.
- Enable HTTPS in CapRover.
- Confirm `/`, `/admin/`, and static CSS load correctly over HTTPS.
