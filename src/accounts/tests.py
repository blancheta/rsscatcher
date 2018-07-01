from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class SignupViewTests(TestCase):

    """
        Test the signup view
    """

    def test_can_display_signup_view(self):

        """
        Can display the login view
        """

        response = self.client.get(reverse('accounts_signup'))
        self.assertEqual(response.status_code, 200)

    def test_can_create_a_user_from_signup_view(self):

        """
        Can create a new user from signup view
        """

        user_count = User.objects.count()

        # Should create a user and redirect to login view
        response = self.client.post(reverse('accounts_signup'), {
            'username': 'alex', 'password': 'passpass',
            'email': 'alexandreblanchet@upidev.fr'
        })

        self.assertEqual(user_count + 1, User.objects.count())
        self.assertRedirects(response, reverse('accounts_login'))

        # Should contain an error
        response = self.client.post(
            reverse('accounts_signup'),
            {
                'username': 'alex', 'password': 'passpass', 'email': 'alexandreblanchet@upidev.fr'
            }
        )

        self.assertTrue(response.context['form'].errors)


class LoginViewTests(TestCase):
    """
    Test the login view
    """

    def setUp(self):
        self.username = "alex"
        self.password = "passpass"
        User.objects.create_user(
            self.username, password=self.password,
            email='alexandreblanchet@upidev.fr', is_active=True
        )

    def test_can_display_login_view(self):

        """
        Can return the login view
        """

        response = self.client.get(reverse('accounts_login'))
        self.assertEqual(response.status_code, 200)

    def test_cannot_authenticate_user_invalid_credentials(self):

        """
        Should fail if incorrect credentials
        """

        response = self.client.post(
            reverse('accounts_signup'),
            {'username': 'alex', 'password': 'passpasspass'}
        )

        self.assertEqual(response.status_code, 200)

    def test_can_authenticate_user(self):

        """
        Can redirect the user to a dashboard view
        """

        response = self.client.post(reverse('accounts_login'), {
            'username': self.username, 'password': self.password
        })

        self.assertEqual(response.status_code, 302)

    def test_redirect_root_to_dashboard_if_user_authenticated(self):

        """
        Can redirect the user to the dashboard if authenticated
        """

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('base-home'))
        self.assertEqual(response.status_code, 302)
