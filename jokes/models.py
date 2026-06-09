from django.db import models


class Joke(models.Model):
    prompt = models.TextField()
    response = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["prompt"]

    def __str__(self):
        return self.prompt
