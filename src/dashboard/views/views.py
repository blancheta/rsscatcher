from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django_markup.markup import formatter
from django.views.generic.list import ListView

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


class FeedPosts(LoginRequiredMixin, ListView):

    context_object_name = 'posts'
    paginate_by = RESULTS_PER_PAGE
    template_name = 'dashboard/feed.html'

    def get_context_data(self, *, object_list=None, **kwargs):

        """
        Return posts for a specific feed
        """

        context = super().get_context_data(**kwargs)

        user = self.request.user
        slug = self.kwargs['slug']

        context['feed'] = Feed.objects.get(subscription__user=user, slug=slug)

        return context

    def get_queryset(self):
        return Post.objects.filter(feed__slug=self.kwargs['slug'])


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


class FilterPosts(LoginRequiredMixin, ListView):

    context_object_name = 'posts'
    paginate_by = RESULTS_PER_PAGE
    template_name = 'dashboard/filtered-posts.html'

    def get_queryset(self):

        filter_state = self.kwargs['filter_state']

        if filter_state == "today":
            today = date.today()
            posts = Post.objects.filter(
                feed__subscription__user=self.request.user,
                published_date__year=today.year,
                published_date__month=today.month,
                published_date__day=today.day,
                userpost__state="unread",
                userpost__user=self.request.user
            )
        else:
            posts = Post.objects.filter(
                userpost__user=self.request.user, userpost__state__exact=filter_state
            )

        return posts


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

