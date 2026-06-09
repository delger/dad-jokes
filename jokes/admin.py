from django.contrib import admin

from .models import Joke


@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = ("prompt", "response", "created_at")
    search_fields = ("prompt", "response")
    readonly_fields = ("created_at",)
