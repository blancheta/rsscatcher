from datetime import date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import Post, Feed


@login_required()
def sidebar(request):

    """
    Render data to display in the sidebar
    """

    today = date.today()

    feeds = [
        {
            'name': feed.name, 'slug': feed.slug, 'posts_count': feed.post_set.count()
        }
        for feed in Feed.objects.filter(subscription__user=request.user)
    ]

    return JsonResponse({
        'feeds': feeds,
        'today-posts-count': Post.objects.filter(
            userpost__user=request.user,
            published_date__year=today.year,
            published_date__month=today.month,
            published_date__day=today.day,
            userpost__state="unread",
        ).count(),
        'read-posts-count': Post.objects.filter(
            userpost__user=request.user,
            userpost__state__exact='read').count(),
        'unread-posts-count': Post.objects.filter(
            userpost__user=request.user,
            userpost__state__exact='unread').count(),
        'readlater-posts-count': Post.objects.filter(
            userpost__user=request.user,
            userpost__state__exact='readlater').count(),
        'favorite-posts-count': Post.objects.filter(
            userpost__user=request.user,
            userpost__state__exact='favorite').count()
    })
