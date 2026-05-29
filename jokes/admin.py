from django.contrib import admin

from .models import Joke


@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at")
    search_fields = ("text",)
    readonly_fields = ("created_at",)
