from __future__ import absolute_import, unicode_literals

from feedparser import parse
from celery.utils.log import get_task_logger
from .celery import app
from base.helpers import slugify
from datetime import datetime
from time import mktime
import pytz

logger = get_task_logger(__name__)

app.conf.beat_schedule = {
    'synchronize-every-10-seconds': {
        'task': 'rsscatcher.tasks.synchronize_posts',
        'schedule': 10.0,
        'args': ()
    },
}

@app.task()
def synchronize_posts():

    """
        Synchronize posts for existing feeds
    """

    from dashboard.models import Feed, Post, UserPost
    from django.contrib.auth.models import User

    feeds = Feed.objects.all()
    logger.info(feeds)

    for feed in feeds:
        last_retrieved_post = Post.objects.filter(feed=feed).order_by('-id').first()

        online_feed = parse(feed.url)
        entries = online_feed.entries

        for entry in entries:

            create_post = True
            slug = slugify(entry.title)
            content = entry.summary

            entry_published_date = datetime.fromtimestamp(mktime(entry.published_parsed))
            entry_published_date = entry_published_date.replace(tzinfo=pytz.utc)

            if last_retrieved_post is not None:

                last_published_date = last_retrieved_post.published_date
                existing_post_count = Post.objects.filter(slug=slug).count()

                if entry_published_date > last_published_date or existing_post_count == 0:
                    create_post = True
                else:
                    create_post = False

            if create_post:

                post = Post.objects.create(
                    name=entry.title,
                    content=content,
                    feed=feed,
                    published_date=entry_published_date,
                    slug=slug,
                    url=entry.link
                )
                # for each subscriber, create a user post
                for user in User.objects.filter(subscription__feed=feed):
                    UserPost.objects.create(post=post,user=user)

                tags = set([tag['term'] for tag in entry.tags if entry.tags])
                for tag in tags:
                    formatted_tag = slugify(tag)
                    feed.keywords.get_or_create(name=formatted_tag)