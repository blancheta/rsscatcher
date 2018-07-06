from time import gmtime
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .tasks import synchronize_posts
from dashboard.models import Feed, Post, Subscription, UserPost, Keyword
from unittest.mock import patch


class FakeEntry(object):

    """
    Mock an entry for the parser
    """

    title = "Title"
    summary = "summary"
    published_parsed = gmtime(500000)
    link = "http://upidev.fr/super-post"

    def __init__(self, title, slug="", tags=[]):
        self.title = title
        self.slug = slug
        self.tags = tags


class FakeParse(object):

    """
    Mock a parser
    """

    entries = []

    def __init__(self):
        self.entries = [
            FakeEntry("Angular X", tags=[{'term': "Linux"}, {'term': "OS"}]),
            FakeEntry("Django 3", tags=[{'term': "Linux"}, {'term': "OS"}]),
            FakeEntry("oooo", slug="oooo")
        ]


class SynchronizePostMethodTests(TestCase):

    """
    Tests the rss parser by mocking
    """

    def get_fakeparser(self, url=None):

        """
        Fake rss feed parser for running tests
        """

        return FakeParse()

    def setUp(self):

        self.feed = Feed.objects.create(
            name="Upidev",
            url="http://feeds.feedburner.com/Upidev",
        )

        self.post = Post.objects.create(
            name="oooo",
            slug="oooo",
            feed=self.feed,
            content="Exampme ...",
            published_date=datetime(2015,5,5)
        )

        self.user = User.objects.create_user("john", email="john@upidev.fr", password="toto")
        UserPost.objects.create(user=self.user,post=self.post)

    @patch("feedparser.parse", get_fakeparser)
    def test_entry_has_a_property_called_tags(self):

        """
        Parser should have a property called tags
        """

        fakeparser_obj = self.get_fakeparser()
        self.assertTrue(fakeparser_obj.entries[0].tags)

    @patch("feedparser.parse", get_fakeparser)
    def test_can_synchronize_posts(self):
        """
        Can synchronize posts for a feed
        """

        synchronize_posts()

        self.assertEqual(Post.objects.count(), 3)

    @patch("feedparser.parse", get_fakeparser)
    def test_create_a_new_post_if_no_existing(self):
        """
        Do not create a new post if already existing
        """

        expected_count = Post.objects.count()

        synchronize_posts()

        actual_count = Post.objects.count()

        self.assertEqual(expected_count + 2, actual_count)

    @patch("feedparser.parse", get_fakeparser)
    def test_create_userpost_for_subscriber(self):
        """
        Create a userpost for feed subscribers
        """

        Subscription.objects.create(user=self.user, feed=self.feed)

        synchronize_posts()

        userpost_count = UserPost.objects.filter(user=self.user).count()

        self.assertEqual(3, userpost_count)

    @patch("feedparser.parse", get_fakeparser)
    def test_create_keywords_for_a_feed(self):
        """
        Add keywords for a feed from post tags
        """

        keywords_count = Keyword.objects.filter(feed=self.feed).count()

        synchronize_posts()

        actual_keywords_count = Keyword.objects.filter(feed=self.feed).count()

        self.assertGreater( actual_keywords_count, keywords_count)

        # Keywords should not be duplicated
        self.assertEqual(actual_keywords_count, 2)












