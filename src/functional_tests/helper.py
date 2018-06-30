import sys
import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from django.contrib.auth import get_user_model
from selenium.webdriver.support.ui import WebDriverWait

User = get_user_model()

DEFAULT_WAIT = 3


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        StaticLiveServerTestCase.setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        StaticLiveServerTestCase.tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
