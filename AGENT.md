Build a minimal Django web app named `dad_jokes`.

Purpose:
- The real purpose is to test Django deployment.
- Keep functionality intentionally minimal.
- Prioritize a clean, reliable production-ready structure over features.

Core user experience:
- User visits home page.
- User sees one dad joke from the database.
- User clicks a button/link to see another random joke.

Required functionality:
- Django project named `dad_jokes_project`
- Django app named `jokes`
- Home page at `/`
- Store jokes in the Django database
- Create a `Joke` model
- Add three starter jokes to the database
- Display a random joke from the database
- Simple HTML template
- Simple CSS file served as a static file
- Django admin enabled for managing jokes

Database requirements:
- Use SQLite initially
- Create and apply migrations
- Add three starter jokes using either:
	- a Django data migration
	or
	- a Django management command
- Jokes should persist in the database

Suggested Joke model:
- `text`
- `created_at`

Production/deployment requirements:
- Use environment variables for:
	- `SECRET_KEY`
	- `DEBUG`
	- `ALLOWED_HOSTS`
- Configure static files correctly
- Use WhiteNoise for serving static files
- Include `requirements.txt`
- Include `.gitignore`
- Include a clear `README.md` with:
	- local setup steps
	- migration commands
	- superuser creation
	- runserver command
	- collectstatic command
	- production environment variables
	- deployment checklist

Recommended files:
- `manage.py`
- `dad_jokes_project/settings.py`
- `dad_jokes_project/urls.py`
- `jokes/models.py`
- `jokes/views.py`
- `jokes/admin.py`
- `jokes/urls.py`
- `jokes/templates/jokes/home.html`
- `jokes/static/jokes/styles.css`
- `requirements.txt`
- `.gitignore`
- `README.md`

Implementation details:
- Use function-based views.
- Use database queries to select a random joke.
- Keep the UI extremely simple.
- Do not add user accounts.
- Do not add JavaScript unless necessary.
- Do not add advanced features.

Home page should include:
- App title: “Dad Jokes”
- One displayed joke
- A button or link: “Another joke”
- A short footer saying: “Built to test Django deployment.”

Starter jokes:
- “I only know 25 letters of the alphabet. I don't know y.”
- “Why did the scarecrow win an award? Because he was outstanding in his field.”
- “What do you call fake spaghetti? An impasta.”

Acceptance tests:
- App runs locally with `poetry run python manage.py runserver`
- Visiting `/` displays a dad joke from the database
- Refreshing or clicking “Another joke” can show a different joke
- Static CSS loads correctly
- `python manage.py collectstatic` works
- App can run with `DEBUG=False`
- WhiteNoise is configured
- Admin can manage jokes
- README explains deployment clearly

After completing the minimal version, suggest optional next steps but do not implement them unless asked:
- Add categories
- Add favorites
- Add ratings
- Add joke submission
- Add tests
- Add PostgreSQL
- Add Docker