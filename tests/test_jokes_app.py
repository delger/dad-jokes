from django.test import TestCase
from django.urls import reverse

from jokes.models import Joke


class JokeModelTests(TestCase):
    def setUp(self):
        Joke.objects.all().delete()

    def test_string_representation_is_joke_prompt(self):
        joke = Joke.objects.create(
            prompt="Why did the test pass?",
            response="It had assertions.",
        )

        self.assertEqual(str(joke), "Why did the test pass?")

    def test_jokes_are_ordered_by_prompt(self):
        Joke.objects.create(prompt="Z joke")
        Joke.objects.create(prompt="A joke")

        self.assertEqual(
            list(Joke.objects.values_list("prompt", flat=True)),
            ["A joke", "Z joke"],
        )


class HomePageTests(TestCase):
    def setUp(self):
        Joke.objects.all().delete()

    def test_home_page_displays_a_joke(self):
        Joke.objects.create(
            prompt="Why did the database laugh?",
            response="It found the query funny.",
        )

        response = self.client.get(reverse("jokes:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dad Jokes")
        self.assertContains(response, "Why did the database laugh?")
        self.assertContains(response, "Show punchline")
        self.assertContains(response, "It found the query funny.")
        self.assertContains(response, "Another joke")
        self.assertContains(response, "/static/jokes/styles.css")

    def test_home_page_displays_one_line_joke_without_punchline_control(self):
        Joke.objects.create(prompt="A database joke.")

        response = self.client.get(reverse("jokes:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A database joke.")
        self.assertNotContains(response, "Show punchline")

    def test_home_page_handles_empty_database(self):
        response = self.client.get(reverse("jokes:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No jokes are in the database yet.")
        self.assertNotIn("recent_joke_ids", self.client.session)

    def test_home_page_does_not_repeat_recent_jokes_until_all_have_been_seen(self):
        jokes = [
            Joke.objects.create(prompt="First joke."),
            Joke.objects.create(prompt="Second joke."),
            Joke.objects.create(prompt="Third joke."),
        ]

        seen_joke_ids = []
        for _ in jokes:
            response = self.client.get(reverse("jokes:home"))

            self.assertEqual(response.status_code, 200)
            seen_joke_ids.append(response.context["joke"].id)

        self.assertCountEqual(seen_joke_ids, [joke.id for joke in jokes])

    def test_home_page_resets_recent_jokes_after_all_jokes_have_been_seen(self):
        joke = Joke.objects.create(prompt="Only joke.")

        first_response = self.client.get(reverse("jokes:home"))
        second_response = self.client.get(reverse("jokes:home"))

        self.assertEqual(first_response.context["joke"], joke)
        self.assertEqual(second_response.context["joke"], joke)
        self.assertEqual(self.client.session["recent_joke_ids"], [joke.id])

    def test_recent_joke_history_is_limited(self):
        jokes = [
            Joke.objects.create(prompt=f"Joke {index}.")
            for index in range(25)
        ]

        for _ in jokes:
            self.client.get(reverse("jokes:home"))

        self.assertEqual(len(self.client.session["recent_joke_ids"]), 20)

    def test_admin_redirects_anonymous_user_to_login(self):
        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/admin/login/?next=/admin/")
