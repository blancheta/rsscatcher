from django.test import TestCase
from django.contrib.auth.models import User
from dashboard.models import Keyword, Feed, Subscription, Post, UserPost, Comment
from datetime import date

class KeywordModelTests(TestCase):

    def setUp(self):
        self.keyword = Keyword.objects.create(name="python")

    def test_create_a_keyword(self):
        self.assertIsInstance(self.keyword, Keyword)

    def test_string_representation(self):
        self.assertEqual(str(self.keyword), self.keyword.name)

def create_a_feed():

    feed = Feed.objects.create(
        name="Python Planet",
        slug="python-planet",
        url="http://feeds.feedburner.com/Upidev"
    )
    feed.keywords.create(name="django")
    feed.keywords.create(name="python")
    feed.keywords.create(name="flask")

    feed.save()

    return feed


class FeedModelTests(TestCase):

    def setUp(self):
        self.feed = create_a_feed()

    def test_can_create_a_feed(self):
        """
        Can create a feed with a name, keywords and a publication_frequency
        """
        self.assertIsInstance(self.feed, Feed)

    def test_string_representation(self):
        self.assertEqual(str(self.feed), self.feed.name)


class SubscriptionModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('alex', password='passpass', email='alexandreblanchet44@gmail.com')
        self.feed = create_a_feed()
        self.subscription = Subscription.objects.create(
            user=self.user,
            feed=self.feed
        )

    def test_can_create_a_subscription(self):
        self.assertIsInstance(self.subscription, Subscription)

    def test_string_representation(self):
        self.assertEqual(str(self.subscription), "{} - {}".format(self.subscription.user.username, self.subscription.feed.name))


class PostModelTests(TestCase):

    def setUp(self):
        feed = create_a_feed()
        self.post = Post.objects.create(
            name="Python 2.7 Countdown",
            content="""
                    Lorem Ipsum is slechts een proeftekst uit het drukkerij-
                    en zetterijwezen. Lorem Ipsum is de standaard proeftekst
                    in deze bedrijfstak sinds de 16e eeuw, toen een onbekende
                    drukker een zethaak met letters nam en ze door elkaar husselde
                    publishing software zoals Aldus PageMaker die versies van Lorem Ipsum bevatten.""",
            feed=feed,
            slug="python-2-7-countdown",
            url="http://www.upidev.fr"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.post), "{} - {}".format(self.post.name, self.post.feed.name))


class UserPostModelTests(TestCase):

    def setUp(self):
        self.feed = create_a_feed()
        self.user = User.objects.create_user('alex',password='passpass', email="alexandreblanchet44@gmail.com")
        self.post = Post.objects.create(
            name="Python 2.7 Countdown",
            content="""
                    Lorem Ipsum is slechts een proeftekst uit het drukkerij-
                    en zetterijwezen. Lorem Ipsum is de standaard proeftekst
                    in deze bedrijfstak sinds de 16e eeuw, toen een onbekende
                    drukker een zethaak met letters nam en ze door elkaar husselde
                    publishing software zoals Aldus PageMaker die versies van Lorem Ipsum bevatten.""",
            feed=self.feed,
            slug="python-2-7-countdown",
            url="http://www.upidev.fr"
        )

        self.userpost = UserPost.objects.create(
            user=self.user,
            post=self.post
        )

    def test_string_representation(self):
        self.assertEqual(str(self.userpost), "{} - {}".format(self.user.username, self.post.name))


class CommentModelTests(TestCase):

    def setUp(self):
        self.feed = create_a_feed()
        self.user = User.objects.create_user('alex', password='passpass', email="alexandreblanchet44@gmail.com")
        self.post = Post.objects.create(
            name="Python 2.7 Countdown",
            content="""
                            Lorem Ipsum is slechts een proeftekst uit het drukkerij-
                            en zetterijwezen. Lorem Ipsum is de standaard proeftekst
                            in deze bedrijfstak sinds de 16e eeuw, toen een onbekende
                            drukker een zethaak met letters nam en ze door elkaar husselde
                            publishing software zoals Aldus PageMaker die versies van Lorem Ipsum bevatten.""",
            feed=self.feed,
            slug="python-2-7-countdown",
            url="http://www.upidev.fr"
        )

        self.userpost = UserPost.objects.create(
            user=self.user,
            post=self.post
        )

        self.parent_comment = Comment.objects.create(
            content="Awesome there !!", user=self.user, post=self.post
        )

    def test_can_create_a_comment(self):
        comment = Comment.objects.create(content="Awesome there !!", user=self.user, post=self.post)
        self.assertIsInstance(comment, Comment)

    def test_can_have_a_comment_parent(self):

        comment = Comment.objects.create(
            content="Awesome there !!", user=self.user, post=self.post, parent=self.parent_comment
        )

        self.assertIsInstance(comment, Comment)

    def test_can_have_a_created_date(self):

        comment = Comment.objects.create(
            content="Awesome there !!", user=self.user, post=self.post,
            parent=self.parent_comment, created_date=date.today()
        )

        self.assertIsInstance(comment, Comment)

    def test_string_representation(self):
        self.assertEqual(str(self.parent_comment), "{} - {}".format(self.user.username, self.parent_comment.content))