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

@register.simple_tag
def most_popular_posts(count=5):
    return Post.published.annotate(comment_count=Count("comments")).order_by("-comment_count")[:count]


@register.inclusion_tag("partials/latest_post.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts
    }
    return context


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.simple_tag
def max_reading_time(count=5):
    return Post.published.aggregate(max_read_time=Max('reading_time'))