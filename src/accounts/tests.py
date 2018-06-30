from django.test import TestCase
from django.test import Client
from django.urls import reverse

from django.contrib.auth.models import User


class SignupViewTests(TestCase):

    def setUp(self):
        self.c = Client()

    def test_can_display_signup_view(self):
        """
        If created, the login view should be returned
        """

        response = self.c.get(reverse('accounts_signup'))
        self.assertEqual(response.status_code, 200)

    def test_can_create_a_user_from_signup_view(self):
        user_count = User.objects.count()

        # Should create a user and redirect to login view
        response = self.c.post(reverse('accounts_signup'), {'username': 'alex', 'password': 'passpass', 'email': 'alexandreblanchet@upidev.fr'})
        self.assertEqual(user_count + 1, User.objects.count())
        self.assertRedirects(response, reverse('accounts_login'))

        # Should contain an error
        response = self.c.post(reverse('accounts_signup'), {'username': 'alex', 'password': 'passpass', 'email': 'alexandreblanchet@upidev.fr'})
        self.assertTrue(response.context['form'].errors)


class LoginViewTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.username = "alex"
        self.password = "passpass"
        User.objects.create_user(self.username, password=self.password, email='alexandreblanchet@upidev.fr', is_active=True)

    def test_can_display_login_view(self):
        """
        If created, the login view should be returned
        """

        response = self.c.get(reverse('accounts_login'))
        self.assertEqual(response.status_code, 200)

    def test_cannot_authenticate_user_invalid_credentials(self):
        # Should redirect the user to a dashboard view
        response = self.c.post(reverse('accounts_signup'), {'username': 'alex', 'password': 'passpasspass'})
        self.assertEqual(response.status_code, 200)

    def test_can_authenticate_user(self):
        # Should redirect the user to a dashboard view
        response = self.c.post(reverse('accounts_login'),
            {'username': self.username, 'password': self.password}
        )

        self.assertEquals(response.status_code, 302)

    def test_redirect_root_to_dashboard_if_user_authenticated(self):
        # Authenticate user
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(reverse('base-home'))
        self.assertEquals(response.status_code, 302)




