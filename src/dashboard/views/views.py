from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_markup.markup import formatter
from rsscatcher.settings import RESULTS_PER_PAGE
from ..models import Feed, Post, UserPost, Comment


def get_comment_root_ids(post):

    """
    Get comments who have no parents for a specific post
    """

    comments = Comment.objects.filter(parent__isnull=True)
    root_comment_ids = ",".join(
        [str(comment.id) for comment in comments if comment.post.id == post.id])

    return root_comment_ids


@login_required()
def feed_posts(request, slug=None):

    """
    Return posts for a specific feed
    """

    posts = create_pagination(
        request, Post.objects.filter(feed__slug=slug), RESULTS_PER_PAGE
    )

    current_feed = Feed.objects.get(subscription__user=request.user, slug=slug)

    return render(request, 'dashboard/feed.html', {
        'posts': posts, 'feed': current_feed
    })


@login_required()
def feed_post(request, slug_feed, slug_post=None):

    """
        Return post for a specific feed
    """

    feed = Feed.objects.get(slug=slug_feed)
    post = Post.objects.get(slug=slug_post, feed=feed)

    if request.POST and request.POST.get('comment-input'):
        content = request.POST.get('comment-input')
        content = formatter(content, filter_name='markdown')
        Comment.objects.create(user=request.user, content=content, post=post)

    return render(request, 'dashboard/post.html', {
        'post': post,
        'state': post.userpost_set.get(user=request.user).state,
        'root_comment_ids': get_comment_root_ids(post)
    })


@login_required()
def post_change_state(request, slug_feed, slug_post=None, state=None):

    """
    Update state for a user post
    """

    feed = Feed.objects.get(slug=slug_feed)
    current_post = Post.objects.get(slug=slug_post, feed=feed)

    if state is not None:
        userpost = UserPost.objects.get(user=request.user, post=current_post)
        userpost.state = state
        userpost.save()

    return render(request, 'dashboard/post.html', {
        'post': current_post, 'state': state,
        'root_comment_ids': get_comment_root_ids(current_post)
    })


def create_pagination(request, entries, entry_number=4):

    """
    Create pagination for views
    which return a list of element to display
    """

    page = request.GET.get('page', 1)
    paginator = Paginator(entries, entry_number)

    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return entries


@login_required()
def filter_view(request, filter_state=None):

    """
    Display posts depending on a filter
    """

    if filter_state == 'today':
        today = date.today()
        posts = Post.objects.filter(
            feed__subscription__user=request.user,
            published_date__year=today.year,
            published_date__month=today.month,
            published_date__day=today.day,
            userpost__state="unread",
            userpost__user=request.user
        )
    else:
        posts = Post.objects.filter(
            userpost__user=request.user, userpost__state__exact=filter_state
        )

    posts = create_pagination(request, posts, RESULTS_PER_PAGE)

    return render(request, 'dashboard/filtered-posts.html', {
        'posts': posts, 'filter': filter_state
    })


@login_required()
def comments_view(request, comment_id, action="reply"):

    """
    Manage edit, reply actions for a comment
    """

    comment = Comment.objects.get(id=comment_id)

    if request.POST and request.POST.get('comment-input'):

        content = request.POST.get('comment-input')
        content = formatter(content, filter_name='markdown')

        if action == "edit" and content:
            comment.content = content
            comment.save()

        elif action == "reply" and request.POST.get('post-id') and content:
            post_id = request.POST.get('post-id')
            Comment.objects.create(
                parent_id=comment_id, user=request.user, content=content, post_id=post_id
            )

    return render(request, 'dashboard/comment.html', {'comment': comment, 'action': action})


