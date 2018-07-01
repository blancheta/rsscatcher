from django.contrib.auth.models import User
from .helper import FunctionalTest
from dashboard.models import Feed, Post, Subscription, UserPost, Comment


class FunctionalScenariosTest(FunctionalTest):

    def create_feeds(self):

        """
          Create fake data for testing projects.
        """	

        feed1 = Feed.objects.create(
            name="Python Galaxy",
            slug="python-galaxy",
            url="http://rss.marketingprofs.com/marketingprofs/graphic-design"
        )

        keyword1 = feed1.keywords.create(name="django")
        keyword2 = feed1.keywords.create(name="python")
        keyword3 = feed1.keywords.create(name="angular")

        feed2 = Feed.objects.create(
            name="Django news",
            slug="django-news",
            url="http://rss.marketingprofs.com/marketingprofs/metrics-roi"
        )
        feed2.keywords.add(keyword1)
        feed2.keywords.add(keyword2)

        feed2.save()

        feed3 = Feed.objects.create(
            name="Angular mania",
            slug="angular-mania",
            url="http://rss.marketingprofs.com/marketingprofs/market-research"
        )
        feed3.keywords.add(keyword3)

        feed3.save()

        post = Post.objects.create(
            name="Python 2.7 Countdown",
            content="""
                            Lorem Ipsum is slechts een proeftekst uit het drukkerij-
                            en zetterijwezen. Lorem Ipsum is de standaard proeftekst
                            in deze bedrijfstak sinds de 16e eeuw, toen een onbekende
                            drukker een zethaak met letters nam en ze door elkaar husselde
                            publishing software zoals Aldus PageMaker die versies van Lorem Ipsum bevatten.""",
            feed=feed1,
            slug="python-2-7-countdown",
            url="http://www.upidev.fr"
        )

        self.username = "alex"
        self.password = "passpass"

        self.user = User.objects.create_user(
            self.username, password=self.password, email='alexandreblanchet44@gmail.com'
        )
        self.user2 = User.objects.create_user(
            'alex2', password='passpass', email='alexandreblanchet44@gmail.com'
        )

        Subscription.objects.create(user=self.user, feed=feed1)

        UserPost.objects.create(user=self.user, post=post)

        Comment.objects.create(user=self.user, content="Awesome!!", post=Post.objects.get(slug='python-2-7-countdown'))
        Comment.objects.create(user=self.user2, content="Nice post", post=Post.objects.get(slug='python-2-7-countdown'))

    def setUp(self):
        self.create_feeds()
        super().setUp()

    def login(self, username, password):
        # He is redirected to a login page
        self.assertEqual(self.browser.title, 'Log in')

        # He sets his username and password and click on login to connect
        self.browser.find_element_by_name('username').send_keys(username)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_id('login').click()

    def logout(self):
        self.browser.find_element_by_id('log-out').click()
        self.assertEqual(self.browser.title, "Welcome")

    def create_an_account_and_login(self):

        # He clicks on "Sign up"
        self.browser.find_element_by_id('sign-up').click()

        username = "alexblanchet"
        password = "passpasspass"

        # He types his fullname, password and email
        self.browser.find_element_by_name('username').send_keys(username)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_name('email').send_keys("alexandreblanchet@upidev.fr")

        # and click on "Create my account"
        self.browser.find_element_by_id('create-account').click()

        # A message appears "You account has been created"
        success_message = self.browser.find_element_by_class_name('alert-success').text
        self.assertEqual(success_message, 'Success! Your account has been created')

        self.login(username, password)

    def search_for_a_specific_feed_by_name(self):
        self.browser.find_element_by_name('search-input').send_keys('Python Galaxy')

        # Then, he clicks on "Search"
        self.browser.find_element_by_id('search-button').click()

        # Feed called "Python Planet" appear
        feeds = self.browser.find_elements_by_class_name('feed')
        self.assertEqual(len(feeds), 1)
        self.assertEqual(feeds[0].find_element_by_class_name('feed-name').text, 'Python Galaxy')

    def search_for_specific_feeds_with_a_keyword(self):
        self.browser.find_element_by_name('search-input').send_keys('Python')

        # Then, he clicks on "Search"
        self.browser.find_element_by_id('search-button').click()

        # Feeds attached to the "python" keyword appear
        feeds = self.browser.find_elements_by_class_name('feed')

        for feed in feeds:
            keywords = feed.find_element_by_class_name('keywords').text
            self.assertTrue('python' in keywords)

    def search_for_a_specific_feed_by_url(self):
        self.browser.find_element_by_name('search-input').send_keys("http://feeds.feedburner.com/Upidev")

        # Then, he clicks on "Search"
        self.browser.find_element_by_id('search-button').click()

        feeds = self.browser.find_elements_by_class_name('feed')

        self.assertEqual(len(feeds), 1)
        self.assertEqual(feeds[0].find_element_by_class_name('feed-name').text, 'Upidev')

    def search_for_specific_feeds(self):
        # He sees a search bar at the top and types "Python"
        self.search_for_a_specific_feed_by_url()
        self.search_for_specific_feeds_with_a_keyword()
        self.search_for_a_specific_feed_by_name()

    def follow_a_feed(self):
        # Alex is interested in a source called "Python Galaxy" clicks on the button "Follow"
        source_block = self.browser.find_element_by_xpath("//div[@id='feed-python-galaxy']")

        source_block.find_element_by_xpath('//button[text()="Follow Me"]').click()

    def read_the_first_post(self):
        post_block = self.browser.find_element_by_id('posts')
        posts = post_block.find_elements_by_class_name('post')
        posts[0].click()

    def read_a_post_for_a_feed(self):
        # The feed appear in Python category in the sidebar
        feed_block = self.browser.find_element_by_xpath("//div[@id='my-feeds']")
        feed_link = feed_block.find_element_by_link_text("Python Galaxy")

        # Alex clicks on "Python Galaxy"
        feed_link.click()

        self.assertEqual(self.browser.title, 'Feed')

        # a list of post appears on the right panel
        post_block = self.browser.find_element_by_xpath("//div[@id='posts']")

        posts = post_block.find_elements_by_class_name('post')
        posts[0].click()

        self.assertEqual(len(posts), 1)

        self.assertEqual(self.browser.title, 'Post')

    def mark_post_as_read(self):
        self.browser.find_element_by_id("marked-as-read").click()

    def mark_post_as_favorite(self):
        self.browser.find_element_by_id("marked-as-favorite").click()

    def mark_post_as_readlater(self):
        self.browser.find_element_by_id("marked-as-readlater").click()

    def filter_read_posts(self):
        self.assertTrue(self.browser.find_element_by_link_text("Already Read"))
        self.browser.find_element_by_id("filter-read").click()

    def filter_unread_posts(self):
        self.assertTrue(self.browser.find_element_by_link_text("Unread"))
        self.browser.find_element_by_id("filter-unread").click()

    def filter_favorite_posts(self):
        self.assertTrue(self.browser.find_element_by_link_text("Favorite"))
        self.browser.find_element_by_id("filter-favorite").click()

    def filter_readlater_posts(self):
        self.assertTrue(self.browser.find_element_by_link_text("To Read Later"))
        self.browser.find_element_by_id("filter-readlater").click()

    def test_read_a_post_for_new_user(self):

        # Alex is interested in Python, Django and Angular and looking
        # for a tool to catch and read rss flows every day

        # By searching on internet, he finds RssCatcher.com and clicks on the link
        self.browser.get(self.server_url)

        # The website is displayed

        # He needs an account on the website and decide to create it
        self.create_an_account_and_login()

        # Alex is now connected and redirected to his dashboard to the discover view
        # Because he hasn't subscribed to feeds yet
        self.assertEqual(self.browser.title, 'Discover')

        # a discover view is displayed

        # Results are directly displayed
        feeds = self.browser.find_elements_by_class_name('feed')

        self.assertEqual(len(feeds), 3)

        self.search_for_specific_feeds()

        self.follow_a_feed()

        self.read_a_post_for_a_feed()

        # Alex is busy and cannot read this interesting post
        # He marks it as readlater
        self.mark_post_as_readlater()
        # Alex clicks on "To Read Later" and check it
        self.filter_readlater_posts()
        self.read_the_first_post()

        # He has some time and read quickly the post
        # He marks it as read
        self.mark_post_as_read()
        # clicks on "Already Read" and check it
        self.filter_read_posts()
        self.read_the_first_post()

        # Alex likes this post
        # He marks it as favourite
        self.mark_post_as_favorite()

        # clicks on "Favorite" and check it
        self.filter_favorite_posts()
        self.read_the_first_post()

    def test_read_an_unread_post_and_add_a_comment(self):

        # Alex registered to RSSCatcher and wants to read news for his favourite feed
        self.browser.get(self.server_url)

        # The website is displayed

        # He authenticates
        self.browser.find_element_by_id('log-in').click()
        self.login(self.username, self.password)

        # Alex is now connected and redirected to his dashboard to the discover view
        # Because he had subscribed to feed
        self.assertEqual(self.browser.title, "Posts filter")

        self.filter_unread_posts()
        self.read_the_first_post()

        # Alex can see comments from other users
        comments = self.browser.find_elements_by_class_name('comment')
        self.assertGreater(len(comments), 0)

        # He adds a comment
        self.browser.find_element_by_name('comment-input').send_keys("Awesome, a very interesting post !")
        self.browser.find_element_by_id('add-comment-button').click()

        refreshed_comments = self.browser.find_elements_by_class_name('comment')

        # The user comment is added in the comment list
        self.assertEqual(len(comments) + 1, len(refreshed_comments))

    def test_read_a_day_post_for_existing_user(self):

        # Alex registered to RSSCatcher and wants to read news for his favourite feed
        self.browser.get(self.server_url)

        # The website is displayed

        # He authenticates
        self.browser.find_element_by_id('log-in').click()
        self.login(self.username, self.password)

        # Alex is now connected and redirected to his dashboard to the discover view
        # Because he hasn't subscribed to feeds yet
        self.assertEqual(self.browser.title, 'Posts filter')

        # # today view is displayed
        self.browser.find_element_by_link_text('Today').click()

        # Results are directly displayed
        posts = self.browser.find_elements_by_class_name('post')

        self.assertEqual(len(posts), 1)

        posts[0].click()

        self.logout()
