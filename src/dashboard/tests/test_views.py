from datetime import datetime, date
from django.test import TestCase
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.paginator import Page
import pytz
from dashboard.models import Feed, Subscription, Post, UserPost, Comment


def init_feed():

    """
    Init Fake data
    """

    feed = Feed.objects.create(
        name="Python Planet",
        slug="python-planet",
        url="http://feeds.feedburner.com/Upidev"
    )

    feed.keywords.create(name="django")
    feed.keywords.create(name="python")
    feed.keywords.create(name="flask")

    Post.objects.create(
        name="Python 2.7 Countdown",
        content="""
            Lorem Ipsum is slechts een proeftekst uit het drukkerij-
            en zetterijwezen. Lorem Ipsum is de standaard proeftekst
            in deze bedrijfstak sinds de 16e eeuw, toen een onbekende
            drukker een zethaak met letters nam en ze door elkaar husselde
            publishing software zoals Aldus PageMaker die versies
            van Lorem Ipsum bevatten.""",
        feed=feed,
        slug="python-2-7-countdown",
        url="http://www.upidev.fr"
    )

    Post.objects.create(
        name="Python 3.4 Countdown",
        content="""
            Lorem Ipsum is slechts een proeftekst uit het drukkerij-
            en zetterijwezen. Lorem Ipsum is de standaard proeftekst
            in deze bedrijfstak sinds de 16e eeuw, toen een onbekende
            drukker een zethaak met letters nam en ze door elkaar husselde
            publishing software zoals Aldus PageMaker die versies
            van Lorem Ipsum bevatten.""",
        feed=feed,
        published_date=datetime(2015, 5, 5, tzinfo=pytz.utc),
        slug="python-3-4-countdown",
        url="http://www.upidev.fr"
    )

    feed.save()

    return feed


def init_users():

    """
    Init fake users
    """

    password = "passpass"
    user = User.objects.create_user(
        "alex", password=password, email='alexandreblanchet@upidev.fr',
        is_active=True
    )
    user2 = User.objects.create_user(
        "alex2", password=password, email='alexandreblanchet@upidev.fr',
        is_active=True
    )

    return[
        {'user': user, 'username': user.username, 'password': password},
        {'user': user2, 'username': user2.username, 'password': password}
    ]


class DashboardViewTests(TestCase):

    def setUp(self):

        self.users = init_users()

        # Authenticate user
        self.client.login(
            username=self.users[0]['username'],
            password=self.users[0]['password'])

    def test_redirect_to_discover_view_if_no_subscriptions_for_user(self):
        """
        If the user is connected and has not feeds
        the discover view should be rendered
        """

        response = self.client.post(reverse('dashboard'))
        self.assertRedirects(response, reverse('dashboard-discover'))

    def test_redirect_to_today_view_if_feeds_for_user(self):
        """
        If the user is connected and has subscriptions
        the today view should be rendered
        """

        Subscription.objects.create(
            feed=init_feed(), user=self.users[0]['user'])

        response = self.client.post(reverse('dashboard'))

        self.assertRedirects(response, "/dashboard/filter/today")


class DiscoverViewTests(TestCase):

    def setUp(self):
        self.feed = init_feed()
        self.users = init_users()

        # Authenticate user
        self.client.login(
            username=self.users[0]['username'],
            password=self.users[0]['password']
        )

    def test_get_sources(self):

        """
        Can get feed sources to the template
        """

        response = self.client.get(reverse('dashboard-discover'))

        self.assertEqual(len(response.context['sources']), 1)
        first_feed = response.context['sources'][0]
        self.assertEqual(first_feed.keywords.count(), 3)

    def test_can_filter_feeds_for_a_keyword(self):

        """
        Can get sources by searching a keyword
        """

        feed2 = Feed.objects.create(
            name="Angular Planet",
            slug="angular-planet",
            url="http://feeds.feedburner.com/Upidev"
        )

        feed2.keywords.create(name="angular")

        python_feed_count = Feed.objects.filter(
            keywords__name="python").count()

        response = self.client.post(
            reverse('dashboard-discover'), {'search-input': 'python'})

        self.assertEqual(len(response.context['sources']), python_feed_count)

    def test_can_filter_feeds_for_a_name(self):

        """
        Can get sources by filtering a name
        """

        python_feed_count = Feed.objects.filter(
            name__iexact="Python Planet").count()

        response = self.client.post(
            reverse('dashboard-discover'), {'search-input': 'Python planet'})

        self.assertEqual(len(response.context['sources']), python_feed_count)

    def test_can_filter_feeds_for_a_known_url(self):

        """
        Can get a feed for a known url
        """

        python_feed_count = Feed.objects.filter(
            url__iexact="http://feeds.feedburner.com/Upidev").count()

        response = self.client.post(
            reverse('dashboard-discover'),
            {'search-input': "http://feeds.feedburner.com/Upidev"}
        )

        self.assertEqual(len(response.context['sources']), python_feed_count)

    def test_can_create_feed_for_an_unknown_url(self):

        """
        Can create a feed for an unknown url
        """

        python_feed_count = Feed.objects.filter(
            url__iexact="http://rss.marketingprofs.com/marketingprofs/graphic-design"
        ).count()

        response = self.client.post(reverse('dashboard-discover'), {
            'search-input': "http://rss.marketingprofs.com/marketingprofs/graphic-design"
        })

        self.assertEqual(
            python_feed_count + 1,
            len(response.context['sources'])
        )

    def test_can_subscribe_to_a_feed(self):

        """
        Can subscribe to a feed
        """

        user = self.users[0]['user']

        user_subscriptions_count = Subscription.objects.filter(
            user=user).count()

        posts_count = Post.objects.filter(feed=self.feed).count()

        self.client.post(
            reverse('dashboard-discover'),
            {'feed-to-follow': self.feed.id, 'following': "no"}
        )

        self.assertEqual(
            user_subscriptions_count + 1,
            Subscription.objects.filter(user=user).count()
        )

        self.assertEqual(UserPost.objects.count(), posts_count)

    def test_can_unsubscribe_for_a_feed(self):

        """
        Can unsubscribe for a feed
        """

        Subscription.objects.create(user=self.users[0]['user'], feed=self.feed)

        self.client.post(
            reverse('dashboard-discover'),
            {'feed-to-follow': self.feed.id, 'following': "yes"}
        )

        with self.assertRaises(ObjectDoesNotExist):
            Subscription.objects.get(
                user=self.users[0]['user'], feed=self.feed)


class FeedViewTests(TestCase):

    def setUp(self):
        self.feed = init_feed()

        self.users = init_users()
        self.user = self.users[0]['user']

        # Authenticate user
        self.client.login(
            username=self.users[0]['username'],
            password=self.users[0]['password']
        )

        Subscription.objects.create(feed=self.feed, user=self.user)

    def test_can_display_posts_for_a_slug(self):

        """
        Can display posts for a slug
        """

        response = self.client.get('/dashboard/feed/python-planet/')
        self.assertEqual(len(response.context['posts']), 2)

    def test_can_display_feed_info_for_slug(self):

        """
        Can display feed info for a slug
        """

        response = self.client.get('/dashboard/feed/python-planet/')
        self.assertTrue(response.context['feed'])
        self.assertIsInstance(response.context['posts'], Page)

    def test_can_display_a_post(self):

        """
        Can display a post
        """

        for post in self.feed.post_set.all():
            UserPost.objects.create(user=self.user, post=post)

        response = self.client.get(
            '/dashboard/feed/python-planet/posts/python-2-7-countdown'
        )

        self.assertTrue(response.context['post'])


class PostViewTests(TestCase):

    def setUp(self):

        feed = init_feed()

        users = init_users()
        self.user = users[0]['user']
        self.user2 = users[1]['user']

        # Authenticate user
        self.client.login(
            username=users[0]['username'],
            password=users[0]['password']
        )

        Subscription.objects.create(feed=feed, user=self.user)
        Subscription.objects.create(feed=feed, user=self.user2)

        for post in Post.objects.filter(feed=feed):
            UserPost.objects.create(post=post, user=self.user)
            UserPost.objects.create(post=post, user=self.user2)

        Comment.objects.create(
            user=self.user,
            content="Awesome!!",
            post=Post.objects.get(slug='python-2-7-countdown')
        )

        Comment.objects.create(
            user=self.user2,
            content="Nice post",
            post=Post.objects.get(slug='python-2-7-countdown')
        )

    def test_marked_post_as_read(self):

        """
        Can mark a post as read
        """

        state = UserPost.objects.get(
            user=self.user, post__slug='python-2-7-countdown').state
        self.assertEqual(state, 'unread')

        self.client.get(
            '/dashboard/feed/python-planet/posts/python-2-7-countdown/read'
        )

        state = UserPost.objects.get(
            user=self.user, post__slug='python-2-7-countdown').state

        self.assertEqual(state, 'read')

    def test_marked_post_as_favorite(self):

        """
        Can mark a post as favourite
        """

        state = UserPost.objects.get(
            user=self.user, post__slug='python-2-7-countdown').state

        self.assertEqual(state, 'unread')

        self.client.get(
            '/dashboard/feed/python-planet/posts/python-2-7-countdown/favorite'
        )

        state = UserPost.objects.get(
            user=self.user, post__slug='python-2-7-countdown').state

        self.assertEqual(state, 'favorite')

    def test_marked_post_as_readlater(self):

        """
        Can mark a post as readlater
        """

        state = UserPost.objects.get(
            user=self.user, post__slug='python-2-7-countdown').state

        self.assertEqual(state, 'unread')

        self.client.get(
            '/dashboard/feed/python-planet/posts/python-2-7-countdown/readlater'
        )

        state = UserPost.objects.get(
            user=self.user, post__slug='python-2-7-countdown').state

        self.assertEqual(state, 'readlater')

    def test_can_return_comments_for_the_post(self):

        """
        Can return comments for a post
        """

        response = self.client.get(
            '/dashboard/feed/python-planet/posts/python-2-7-countdown'
        )

        self.assertTrue(response.context['root_comment_ids'])

    def test_can_add_a_comment(self):

        """
        Can add a comment
        """

        comment_count = Comment.objects.count()
        comment_count_expected = comment_count + 1

        response = self.client.post(
            '/dashboard/feed/python-planet/posts/python-2-7-countdown',
            {'comment-input': "Awesome dude"}
        )

        self.assertEqual(
            comment_count_expected,
            response.context['post'].comment_set.count()
        )


class FilterViewTests(TestCase):

    def setUp(self):

        feed = init_feed()

        users = init_users()
        self.user = users[0]['user']
        self.user2 = users[1]['user']

        Subscription.objects.create(feed=feed, user=self.user)
        Subscription.objects.create(feed=feed, user=self.user2)

        # Authenticate user
        self.client.login(
            username=users[0]['username'], password=users[0]['password']
        )

        self.userpost = UserPost.objects.create(
            user=self.user, post=Post.objects.get(slug="python-2-7-countdown")
        )

        UserPost.objects.create(
            user=self.user2, post=Post.objects.get(slug="python-2-7-countdown")
        )

    def test_can_filter_day_posts(self):

        """
        Can filter posts of the day
        """

        response = self.client.get('/dashboard/filter/today')

        posts = response.context['posts']
        for post in posts:
            self.assertEqual(post.published_date.date(), date.today())
            userpost = UserPost.objects.get(user=self.user, post=post)
            self.assertEqual(userpost.state, "unread")

        self.assertIsInstance(response.context['posts'], Page)

    def test_can_filter_read_posts(self):

        """
        Can filter read posts
        """

        self.userpost.state = 'read'
        self.userpost.save()

        response = self.client.get('/dashboard/filter/read')

        posts = response.context['posts']

        for post in posts:
            self.assertEqual(
                UserPost.objects.get(user=self.user, post=post).state,
                'read'
            )

        self.assertIsInstance(response.context['posts'], Page)

    def test_can_filter_unread_posts(self):

        """
        Can filter unread posts
        """

        response = self.client.get('/dashboard/filter/unread')

        posts = response.context['posts']

        for post in posts:
            self.assertEqual(
                UserPost.objects.get(user=self.user, post=post).state,
                'unread'
            )

        self.assertIsInstance(response.context['posts'], Page)

    def test_can_filter_favorite_posts(self):

        """
        Can filter favorite posts
        """

        self.userpost.state = 'favorite'
        self.userpost.save()

        response = self.client.get('/dashboard/filter/favorite')

        posts = response.context['posts']

        for post in posts:
            self.assertEqual(
                UserPost.objects.get(user=self.user, post=post).state,
                'favorite'
            )

        self.assertIsInstance(response.context['posts'], Page)


class CommentViewTests(TestCase):

    def setUp(self):
        init_feed()

        users = init_users()
        self.user = users[0]['user']
        self.post = Post.objects.get(slug='python-2-7-countdown')

        self.client.login(
            username=users[0]['username'],
            password=users[0]['password']
        )

        self.comment = Comment.objects.create(
            user=self.user, content="Awesome!!", post=self.post
        )

    def test_can_edit_a_comment(self):

        """
        Can edit a comment
        """

        response = self.client.post(
            '/dashboard/comments/{}/edit'.format(self.comment.id),
            {'comment-input': 'toto'}
        )

        self.assertEqual(
            Comment.objects.get(id=self.comment.id).content, '<p>toto</p>')

        self.assertEqual(response.status_code, 200)

    def test_can_reply_for_a_comment(self):

        """
        Can reply for a comment
        """

        comments_count = Comment.objects.filter(post=self.post).count()

        response = self.client.post(
            '/dashboard/comments/{}/reply'.format(self.comment.id),
            {
                'comment-input': 'olé',
                'post-id': self.post.id
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            comments_count + 1,
            Comment.objects.filter(post=self.post).count()
        )
