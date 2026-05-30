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

        fixture_texts = self._load_fixture_texts(fixture_path)
        existing_texts = set(Joke.objects.values_list("text", flat=True))
        desired_texts = set(fixture_texts)

        to_create = sorted(desired_texts - existing_texts)
        to_delete = sorted(existing_texts - desired_texts)

        if options["dry_run"]:
            self.stdout.write(
                f"Would create {len(to_create)} jokes and delete {len(to_delete)} jokes."
            )
            return

        with transaction.atomic():
            if to_delete:
                Joke.objects.filter(text__in=to_delete).delete()
            Joke.objects.bulk_create(Joke(text=text) for text in to_create)

        self.stdout.write(
            self.style.SUCCESS(
                f"Synced jokes from {fixture_path}: "
                f"{len(to_create)} created, {len(to_delete)} deleted, "
                f"{len(desired_texts)} total."
            )
        )

    def _load_fixture_texts(self, fixture_path):
        try:
            with fixture_path.open(encoding="utf-8") as fixture_file:
                objects = json.load(fixture_file)
        except json.JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON fixture: {exc}") from exc

        if not isinstance(objects, list):
            raise CommandError("Fixture must contain a list of objects.")

        texts = []
        for index, item in enumerate(objects):
            if not isinstance(item, dict):
                raise CommandError(f"Fixture item {index} must be an object.")
            if item.get("model") != "jokes.joke":
                continue

            fields = item.get("fields")
            if not isinstance(fields, dict) or not fields.get("text"):
                raise CommandError(f"Fixture item {index} is missing fields.text.")
            texts.append(fields["text"])

        if not texts:
            raise CommandError("Fixture contains no jokes.joke records.")

        duplicates = sorted({text for text in texts if texts.count(text) > 1})
        if duplicates:
            raise CommandError(
                "Fixture contains duplicate joke text: " + "; ".join(duplicates)
            )

        return texts
