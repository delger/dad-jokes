import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from jokes.models import Joke


class Command(BaseCommand):
    help = "Sync jokes from an exported JSON fixture."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fixture",
            default="fixtures/jokes.json",
            help="Path to a Django JSON fixture, relative to BASE_DIR by default.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report changes without writing to the database.",
        )

    def handle(self, *args, **options):
        fixture_path = Path(options["fixture"])
        if not fixture_path.is_absolute():
            fixture_path = Path(settings.BASE_DIR) / fixture_path

        if not fixture_path.exists():
            raise CommandError(f"Fixture not found: {fixture_path}")

        fixture_jokes = self._load_fixture_jokes(fixture_path)
        existing_jokes = set(Joke.objects.values_list("prompt", "response"))
        desired_jokes = set(fixture_jokes)

        to_create = sorted(desired_jokes - existing_jokes)
        to_delete = sorted(existing_jokes - desired_jokes)

        if options["dry_run"]:
            self.stdout.write(
                f"Would create {len(to_create)} jokes and delete {len(to_delete)} jokes."
            )
            return

        with transaction.atomic():
            if to_delete:
                for prompt, response in to_delete:
                    Joke.objects.filter(prompt=prompt, response=response).delete()
            Joke.objects.bulk_create(
                Joke(prompt=prompt, response=response)
                for prompt, response in to_create
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Synced jokes from {fixture_path}: "
                f"{len(to_create)} created, {len(to_delete)} deleted, "
                f"{len(desired_jokes)} total."
            )
        )

    def _load_fixture_jokes(self, fixture_path):
        try:
            with fixture_path.open(encoding="utf-8") as fixture_file:
                objects = json.load(fixture_file)
        except json.JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON fixture: {exc}") from exc

        if not isinstance(objects, list):
            raise CommandError("Fixture must contain a list of objects.")

        jokes = []
        for index, item in enumerate(objects):
            if not isinstance(item, dict):
                raise CommandError(f"Fixture item {index} must be an object.")
            if item.get("model") != "jokes.joke":
                continue

            fields = item.get("fields")
            if not isinstance(fields, dict) or not fields.get("prompt"):
                raise CommandError(f"Fixture item {index} is missing fields.prompt.")
            jokes.append((fields["prompt"], fields.get("response", "")))

        if not jokes:
            raise CommandError("Fixture contains no jokes.joke records.")

        duplicates = sorted({joke for joke in jokes if jokes.count(joke) > 1})
        if duplicates:
            raise CommandError(
                "Fixture contains duplicate jokes: "
                + "; ".join(prompt for prompt, response in duplicates)
            )

        return jokes
