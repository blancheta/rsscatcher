from django import template
from django.utils.safestring import mark_safe
from ..models import Subscription, Comment

register = template.Library()


@register.simple_tag()
def is_followed(feed_id, user_id):
    return bool(Subscription.objects.filter(user__id=user_id, feed__id=feed_id).count())


@register.simple_tag()
def comments(comment_ids, height, is_root_call, current_user_id):
    global_content = ""
    for comment in comment_ids.split(','):
        content = ""
        global_content += create_comment_tree(comment, height, is_root_call, content, current_user_id)

    return mark_safe(global_content)


def create_comment_tree(node_id, height, is_root_call, content, current_user_id):

    """
    Create a tree of comments.
    Comments can have an infinite number of comment children

    :param node_id: Post id
    :param height:
    :param is_root_call:
    :param content:
    :param current_user_id:
    :return: content
    """

    node = Comment.objects.get(id=node_id)
    spacing = 14

    if is_root_call:
        is_root_call = False
    else:
        height += 1

    line = "<div class='comment comment-"+ str(height) +"'>"
    comment_block = "<b>{}</b>".format(node.user.username)

    if current_user_id == node.user_id:
        # if node.created_date:
        #     comment_block += " {:%d, %b %Y at %H:%M}".format(node.created_date)
        comment_block += " | <a href='{}'> Edit </a>".format("/dashboard/comments/" + str(node.id) + "/edit")
    else:
        comment_block += " | <a href='{}'> Reply </a>".format("/dashboard/comments/" + str(node.id) + "/reply")

    comment_block += "<br>"
    comment_block += "<div class='comment-content'>" + node.content + "</div>"

    line += comment_block

    content += "</div>"
    content += line

    if node.comment_set.count():
        children = node.comment_set.all()

        for child in children:
            if child is not None:
                content = create_comment_tree(child.id, height, is_root_call, content, current_user_id)

    return content