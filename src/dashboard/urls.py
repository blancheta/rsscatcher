from django.urls import path
from .views import (
    dashboard, filter_view, discover, feed_posts,
    feed_post, post_change_state, sidebar, comments_view
)

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('filter/<filter_state>', filter_view, name="dashboard-filter"),
    path('discover/', discover, name="dashboard-discover"),
    path('sidebar/', sidebar, name="dashboard-sidebar"),
    path('comments/<comment_id>/<action>', comments_view, name="dashboard-comments"),
    path('feed/<slug>/', feed_posts, name='dashboard-feed-posts'),
    path('feed/<slug_feed>/posts/<slug_post>', feed_post, name='dashboard-feed-post'),
    path('feed/<slug_feed>/posts/<slug_post>/<state>',
         post_change_state, name='dashboard-post-change-state')
]
