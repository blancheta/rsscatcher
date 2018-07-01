"""
Register models for admin views
"""

from django.contrib import admin
from .models import Keyword, Feed, Post, Subscription, UserPost, Comment

admin.site.register(Keyword)
admin.site.register(Feed)
admin.site.register(Subscription)
admin.site.register(Post)
admin.site.register(UserPost)
admin.site.register(Comment)
