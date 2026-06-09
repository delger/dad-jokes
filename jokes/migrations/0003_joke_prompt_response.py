from django.db import migrations, models


def split_prompt_response(apps, schema_editor):
    Joke = apps.get_model("jokes", "Joke")
    for joke in Joke.objects.all():
        prompt = joke.prompt.strip()
        response = ""
        if "?" in prompt:
            setup, punchline = prompt.split("?", 1)
            if punchline.strip():
                prompt = f"{setup.strip()}?"
                response = punchline.strip()
        joke.prompt = prompt
        joke.response = response
        joke.save(update_fields=["prompt", "response"])


def join_prompt_response(apps, schema_editor):
    Joke = apps.get_model("jokes", "Joke")
    for joke in Joke.objects.all():
        prompt = joke.prompt.strip()
        response = joke.response.strip()
        joke.prompt = f"{prompt} {response}".strip()
        joke.save(update_fields=["prompt"])


class Migration(migrations.Migration):
    dependencies = [
        ("jokes", "0002_starter_jokes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="joke",
            old_name="text",
            new_name="prompt",
        ),
        migrations.AddField(
            model_name="joke",
            name="response",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterModelOptions(
            name="joke",
            options={"ordering": ["prompt"]},
        ),
        migrations.RunPython(split_prompt_response, join_prompt_response),
    ]
