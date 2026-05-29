# Dad Jokes

A minimal Django app for testing deployment. The home page displays one random dad joke from the database and links back to itself to show another joke.

## Local Setup

Install dependencies with Poetry:

```bash
poetry install
```

Or use `requirements.txt` with a virtual environment:

```bash
python -m pip install -r requirements.txt
```

## Database

Create and apply migrations:

```bash
poetry run python manage.py migrate
```

The `jokes` app includes a data migration that inserts three starter jokes. Jokes are stored in SQLite by default at `db.sqlite3`.

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
poetry run python manage.py collectstatic
```

WhiteNoise is configured to serve collected static files.

## Production Environment Variables

Set these environment variables in production:

```bash
SECRET_KEY=replace-with-a-secure-secret
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
```

`ALLOWED_HOSTS` is a comma-separated list. SQLite is configured initially; use a persistent disk or switch databases before deploying to a platform with ephemeral storage.

## Deployment Checklist

- Install dependencies from `requirements.txt` or Poetry.
- Set `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS`.
- Run `python manage.py migrate`.
- Run `python manage.py collectstatic --noinput`.
- Create a superuser if admin access is needed.
- Start the app with a WSGI server pointed at `dad_jokes_project.wsgi:application`.
- Confirm `/`, `/admin/`, and static CSS load correctly.
