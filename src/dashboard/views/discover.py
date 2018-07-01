from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from feedparser import parse
from base.helpers import slugify
from ..models import Feed, Subscription, Post, UserPost


def create_a_feed(url):
    """
    Create a feed for an unknown source
    """

    new_feed = parse(url)

    if new_feed.feed.title:

        Feed.objects.create(
            name=new_feed.feed.title,
            slug=slugify(new_feed.feed.title),
            url=new_feed.url
        )


@login_required()
def discover(request):

    """
    Discover view to manage feed user subscriptions
    """

    sources = Feed.objects.all()

    if request.POST:
        if request.POST.get('search-input', False):
            search_term = request.POST['search-input']

            sources = Feed.objects.filter(
                Q(name__iexact=search_term)
            )

            if not sources:
                sources = Feed.objects.filter(
                    keywords__name__iexact=search_term
                )

            if not sources:
                sources = Feed.objects.filter(
                    url__exact=search_term
                )

                if not sources:
                    # Create the feed form search_term
                    create_a_feed(search_term)

                    sources = Feed.objects.filter(
                        url__exact=search_term
                    )

        if request.POST.get('feed-to-follow', False):
            feed_to_subscribe = Feed.objects.get(id=request.POST['feed-to-follow'])

            if request.POST['following'] == "no":
                Subscription.objects.create(
                    user=request.user,
                    feed=feed_to_subscribe
                )

                # Attached user for posts of the feed
                for post in Post.objects.filter(feed=feed_to_subscribe):
                    UserPost.objects.create(
                        post=post,
                        user=request.user
                    )
            else:
                Subscription.objects.filter(
                    user=request.user,
                    feed=feed_to_subscribe
                ).delete()

                UserPost.objects.filter(
                    user=request.user, post__feed__exact=feed_to_subscribe).delete()

    return render(request, 'dashboard/discover.html', {'sources': sources})
