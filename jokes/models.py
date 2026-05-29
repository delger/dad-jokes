from django.db import models


class Joke(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["text"]

    def __str__(self):
        return self.text
