from django import template
from blog.models import *

register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.objects.count()

@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def last_post_date():
    return Post.published.last().publish