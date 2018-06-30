from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User


class HomeViewTests(TestCase):

    def test_authenticated_user_is_redirected_to_dashboard(self):
        password = "passpass"
        username="alex"
        self.user = User.objects.create_user(username, password=password, email='alexandreblanchet@upidev.fr', is_active=True)
        self.client.login(username=username, password=password)
        self.response = self.client.get(reverse('base-home'))
        self.assertEquals(self.response.status_code, 302)