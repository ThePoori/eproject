from django import template
from blog.models import *

register = template.Library()

# get post count
@register.simple_tag()
def total_posts():
    return Post.objects.count()

# get comment count
@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()

# get last post by date
@register.simple_tag()
def last_post_date():
    return Post.published.last().publish