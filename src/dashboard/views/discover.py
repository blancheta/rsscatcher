from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from feedparser import parse
from django.utils.text import slugify
from ..models import Feed, Subscription, Post, UserPost
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def create_a_feed(url):
    """
    Create a feed for an unknown source
    """

    new_feed = parse(url)
    title = new_feed.feed.title
    url = new_feed.url

    Feed.objects.create(
        name=title,
        slug=slugify(title),
        url=url
    )


@login_required()
def discover(request):

    """
    Discover view to manage feed user subscriptions
    """

    sources = []

    if request.POST:
        if request.POST.get('search-input', False):
            search_term = request.POST['search-input']

            # Check if a source exist for this term
            sources = Feed.objects.filter(
                Q(name__iexact=search_term) |
                Q(url=search_term) |
                Q(keywords__name=search_term)
            ).distinct()

            if not sources:
                val = URLValidator()
                try:
                    val(search_term)

                    # New feed from the valid URL
                    create_a_feed(search_term)

                    # Filter on this new feed
                    sources = Feed.objects.filter(
                        url__iexact=search_term
                    )

                except ValidationError:
                   print("search_term is not a valid URL")

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

    if not sources:
        sources = Feed.objects.all()

    return render(request, 'dashboard/discover.html', {'sources': sources})
