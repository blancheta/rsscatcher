from django.urls import path
from .views import (
    dashboard, FilterPosts, FeedPosts,
    FeedPost, PostChangeState, CommentView, DiscoverView, sidebar, FeedPostNewComment
)

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('filter/<filter_state>', FilterPosts.as_view(), name="dashboard-filter"),
    path('discover/', DiscoverView.as_view(), name="dashboard-discover"),
    path('sidebar/', sidebar, name="dashboard-sidebar"),
    path('comments/<comment_id>/<action>', CommentView.as_view(), name="dashboard-comments"),
    path('feed/<slug>/', FeedPosts.as_view(), name='dashboard-feed-posts'),
    path('feed/<slug_feed>/posts/<slug_post>', FeedPost.as_view(), name='dashboard-feed-post'),
    path('comment/<slug_feed>/<slug_post>/create', FeedPostNewComment.as_view(), name='dashboard-post-new-comment'),
    path('feed/<slug_feed>/posts/<slug_post>/<state>', PostChangeState.as_view(), name='dashboard-post-change-state')
]
