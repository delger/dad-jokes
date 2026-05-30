from django.test import TestCase
from django.urls import reverse

from jokes.models import Joke


class JokeModelTests(TestCase):
    def setUp(self):
        Joke.objects.all().delete()

    def test_string_representation_is_joke_text(self):
        joke = Joke.objects.create(text="Why did the test pass? It had assertions.")

        self.assertEqual(str(joke), "Why did the test pass? It had assertions.")

    def test_jokes_are_ordered_by_text(self):
        Joke.objects.create(text="Z joke")
        Joke.objects.create(text="A joke")

        self.assertEqual(
            list(Joke.objects.values_list("text", flat=True)),
            ["A joke", "Z joke"],
        )


class HomePageTests(TestCase):
    def setUp(self):
        Joke.objects.all().delete()

    def test_home_page_displays_a_joke(self):
        Joke.objects.create(text="A database joke.")

        response = self.client.get(reverse("jokes:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dad Jokes")
        self.assertContains(response, "A database joke.")
        self.assertContains(response, "Another joke")
        self.assertContains(response, "/static/jokes/styles.css")

    def test_home_page_handles_empty_database(self):
        response = self.client.get(reverse("jokes:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No jokes are in the database yet.")

    def test_admin_redirects_anonymous_user_to_login(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/admin/login/?next=/admin/")
