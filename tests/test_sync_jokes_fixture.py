import json
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from jokes.models import Joke


class SyncJokesFixtureTests(TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.fixture_dir = self.base_dir / "fixtures"
        self.fixture_dir.mkdir(exist_ok=True)
        self.fixture_path = self.fixture_dir / "jokes.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_fixture(self, texts):
        objects = [
            {
                "model": "jokes.joke",
                "pk": index,
                "fields": {
                    "text": text,
                    "created_at": "2026-01-01T00:00:00Z",
                },
            }
            for index, text in enumerate(texts, start=1)
        ]
        self.fixture_path.write_text(json.dumps(objects), encoding="utf-8")

    def test_sync_creates_missing_and_deletes_stale_jokes(self):
        Joke.objects.create(text="stale joke")
        Joke.objects.create(text="existing joke")
        self.write_fixture(["existing joke", "new joke"])

        with override_settings(BASE_DIR=self.base_dir):
            call_command(
                "sync_jokes_fixture",
                fixture="fixtures/jokes.json",
                stdout=StringIO(),
            )

        self.assertEqual(
            list(Joke.objects.order_by("text").values_list("text", flat=True)),
            ["existing joke", "new joke"],
        )

    def test_duplicate_fixture_text_raises_error(self):
        self.write_fixture(["same joke", "same joke"])

        with override_settings(BASE_DIR=self.base_dir), self.assertRaises(CommandError):
            call_command("sync_jokes_fixture", fixture="fixtures/jokes.json")
