# Dad Jokes

A minimal Django app for testing deployment. The home page displays one random dad joke from the database and links back to itself to show another joke.

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

Local development uses SQLite by default at `db.sqlite3`.

Create and apply local migrations:

```bash
poetry run python manage.py migrate
```

The `jokes` app includes a data migration that inserts three starter jokes.

## Production Database

Production uses Postgres through `DATABASE_URL`. Create a Postgres database in CapRover, then set `DATABASE_URL` for the app:

```bash
DATABASE_URL=postgres://USER:PASSWORD:HOST:5432/DBNAME
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
  dad-jokes
```

The container runs migrations, collects static files, and starts Gunicorn on port `80`.

## Production Environment Variables

Set these environment variables in production:

```bash
SECRET_KEY=replace-with-a-secure-secret
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_URL=postgres://USER:PASSWORD:HOST:5432/DBNAME
```

`ALLOWED_HOSTS` is a comma-separated list. SQLite is only the local default; production should use Postgres.

## Deployment Path

1. Build locally.
2. Dockerize the app.
3. Deploy with CapRover.
4. Attach the domain.
5. Enable HTTPS.

## Deployment Checklist

- Confirm the app runs locally with `poetry run python manage.py runserver`.
- Build and test the Docker image locally.
- Create or attach a Postgres database in CapRover.
- Set production environment variables in CapRover: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and `DATABASE_URL`.
- Deploy the app through CapRover using `captain-definition`.
- Confirm the container startup runs migrations and collects static files.
- Create a superuser if admin access is needed.
- Attach the custom domain in CapRover.
- Enable HTTPS in CapRover.
- Confirm `/`, `/admin/`, and static CSS load correctly over HTTPS.
