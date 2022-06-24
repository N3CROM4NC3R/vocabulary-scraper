from django.test import TestCase
from django.urls import reverse

from scrapper.models import CustomUser as User

# Create your tests here.


class LandingPageViewTest(TestCase):

    def test_user_can_see_landing_page(self):

        response = self.client.get(reverse("scrapper:landingPage"))

        self.assertEqual(response.status_code,200)

        self.assertContains(response,"Create Vocabulary Decks")


    """ def test_logged_user_cant_see_landing_page(self):

        user = User.objects.create_user(username="admin")
        user.set_password("12345")
        user.save()


        login = self.client.login(username = "admin",password = "12345")
        
        response = self.client.get(reverse("scrapper:landingPage"))

        self.assertEqual(response.status_code,"308") """

        
class LoginViewTest(TestCase):
    def test_guest_can_access_page(self):
        response = self.client.get(reverse("scrapper:login"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'scrapper/login.html')




    def test_guest_can_log_in(self):

        user = User.objects.create_user(username="admin")
        user.set_password("12345")
        user.save()

        login = self.client.login(username = "admin",password = "12345")

        self.assertTrue(login)