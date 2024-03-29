from django.test import TestCase, RequestFactory
from django.urls import reverse
from scraper.utils import get_number_words
import json

from scraper.models import CustomUser as User

# Create your tests here.


class LandingPageViewTest(TestCase):

    def test_user_can_see_landing_page(self):

        response = self.client.get(reverse("scraper:landingPage"))

        self.assertEqual(response.status_code,200)

        self.assertContains(response,"Create Vocabulary Decks")


    """ def test_logged_user_cant_see_landing_page(self):

        user = User.objects.create_user(username="admin")
        user.set_password("12345")
        user.save()


        login = self.client.login(username = "admin",password = "12345")
        
        response = self.client.get(reverse("scraper:landingPage"))

        self.assertEqual(response.status_code,"308") """

        
class LoginViewTest(TestCase):
    def test_guest_can_access_page(self):
        response = self.client.get(reverse("scraper:login"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'scraper/pages/login.html')


    def test_guest_can_log_in(self):

        user = User.objects.create_user(username="admin")
        user.set_password("12345")
        user.save()

        login = self.client.login(username = "admin",password = "12345")

        self.assertTrue(login)

class TranslationViewTest(TestCase):

    def logged_user(self):
        user = User.objects.create_user(username="testuser")
        user.set_password("12345")
        user.save()

        self.client.login(username="testuser",password="12345")

        return user


    def test_guest_cant_access_page(self):

        response = self.client.get(reverse("scraper:translations"))
        
        self.assertEqual(response.status_code, 302)

    def test_logged_user_can_access_page(self):

        user = self.logged_user()

        response = self.client.get(reverse("scraper:translations"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "scraper/pages/translations.html")

    def test_logged_user_can_create_a_deck_with_translated_words(self):
        
        user = self.logged_user()

        deck_name = "vocabulary"

        words = ["get"]

        data = {
            "deck_name" : deck_name,
            "words" : words,
            "principal-translation": True,
            "additional-translation": True,
            "compound-form" : True,
            "verbal-elocution": True,
        }

        json_data = json.dumps(data)

        response = self.client.post(reverse("scraper:translations"),json_data,content_type="application/json")

        self.assertEqual(response.status_code, 200)
        
        json_response = json.loads(response.content)
        redirected_url = json_response["downloadUrl"]

        self.assertIn("https://res.cloudinary.com", redirected_url)


    def test_logged_user_is_redirected_when_access_login_page(self):

        user = self.logged_user()

        response = self.client.get(reverse("scraper:login"))

        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'], reverse("scraper:translations"))

