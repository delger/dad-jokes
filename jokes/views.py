from django.shortcuts import render

from .models import Joke


def home(request):
    joke = Joke.objects.order_by("?").first()
    return render(request, "jokes/home.html", {"joke": joke})
