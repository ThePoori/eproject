from django import template
from blog.models import *
from django.db.models import Count, Max, Min
from markdown import markdown
from django.utils.safestring import mark_safe

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

# use annotate in templatetags
@register.simple_tag
def most_popular_posts(count=5):
    return Post.published.annotate(comment_count=Count("comments")).order_by("-comment_count")[:count]

# use inclusion tag
@register.inclusion_tag("partials/latest_post.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context

# use filter to markdown
@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))

# just practice
# @register.simple_tag
# def max_reading_time(count=5):
#     return Post.published.aggregate(max_read_time=Max('reading_time'))


@register.simple_tag
def max_reading_time():
    max_time = Post.published.aggregate(max_val=Max('reading_time'))['max_val']
    if max_time is not None:
        post = Post.published.filter(reading_time=max_time).first()
        return post
    return None


@register.simple_tag
def min_reading_time():
    min_time = Post.published.aggregate(min_val=Min('reading_time'))['min_val']
    if min_time is not None:
        post = Post.published.filter(reading_time=min_time).first()
        return post
    return None

# filter words
import re
@register.filter
def censor(value):
    if not isinstance(value, str):
        return value
    bad_words = ['fuck', 'shet', 'bitch', 'applepulisher']
    for word in bad_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        value = pattern.sub('*' * len(word), value)
    return value

from django.contrib.auth import get_user_model
User = get_user_model()
@register.simple_tag
def most_popular_author(count=5):
    top_users = User.objects.annotate(post_count=Count("user_posts")).order_by("-post_count")[:count]
    if top_users:
        return Post.published.filter(author__in=top_users).select_related("author").order_by('-publish')
    return Post.published.none()