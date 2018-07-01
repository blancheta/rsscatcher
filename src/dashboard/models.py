from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Keyword(models.Model):

    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class Feed(models.Model):
    name = models.CharField(max_length=60, verbose_name=_("Name"))
    slug = models.CharField(max_length=60, verbose_name=_("Slug"))
    keywords = models.ManyToManyField(Keyword, default=[])
    DAILY = 'everyday'
    WEEKLY = 'everyweek'
    MONTHLY = 'everymonth'
    FREQUENCY_CHOICES = (
        (DAILY, 'Every day'),
        (WEEKLY, 'Every week'),
        (MONTHLY, 'Every month'),
    )
    publication_frequency = models.CharField(
        max_length=40, choices=FREQUENCY_CHOICES, default=MONTHLY
    )
    url = models.URLField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.feed.name)


class Post(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    slug = models.CharField(max_length=200, verbose_name=_("Slug"))
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return "{} - {}".format(self.name, self.feed.name)

    class Meta:
        ordering = ["-id"]


class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    READ = 'read'
    UNREAD = 'unread'
    READLATER = 'readlater'
    FAVORITE = 'favorite'
    STATE_CHOICES = (
        (READ, 'Read'),
        (UNREAD, 'Unread'),
        (READLATER, 'Read Later'),
        (FAVORITE, 'Favorite')
    )
    state = models.CharField(
        max_length=100, choices=STATE_CHOICES, default=UNREAD
    )

    def __str__(self):
        return "{} - {}".format(self.user.username, self.post.name)


class Comment(models.Model):

    """
        A comment has a user and a post.
        If a user post is deleted, the user comment will survive
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.user.username, self.content)
