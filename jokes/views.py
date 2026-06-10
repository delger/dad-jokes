from django.shortcuts import render

from .models import Joke


RECENT_JOKE_SESSION_KEY = "recent_joke_ids"
RECENT_JOKE_LIMIT = 20


def home(request):
    joke = get_random_joke(request)
    return render(request, "jokes/home.html", {"joke": joke})


def get_random_joke(request):
    recent_joke_ids = request.session.get(RECENT_JOKE_SESSION_KEY, [])
    available_jokes = Joke.objects.exclude(id__in=recent_joke_ids)

    joke = available_jokes.order_by("?").first()
    if joke is None:
        joke = Joke.objects.order_by("?").first()
        recent_joke_ids = []

    if joke is not None:
        recent_joke_ids = [joke.id, *recent_joke_ids]
        request.session[RECENT_JOKE_SESSION_KEY] = recent_joke_ids[
            :RECENT_JOKE_LIMIT
        ]

    return joke
