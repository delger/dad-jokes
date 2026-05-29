from django.db import migrations


STARTER_JOKES = [
    "I only know 25 letters of the alphabet. I don't know y.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "What do you call fake spaghetti? An impasta.",
]


def add_starter_jokes(apps, schema_editor):
    Joke = apps.get_model("jokes", "Joke")
    for text in STARTER_JOKES:
        Joke.objects.get_or_create(text=text)


def remove_starter_jokes(apps, schema_editor):
    Joke = apps.get_model("jokes", "Joke")
    Joke.objects.filter(text__in=STARTER_JOKES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("jokes", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_starter_jokes, remove_starter_jokes),
    ]
