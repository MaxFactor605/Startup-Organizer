from io import StringIO
from django import template

register = template.Library()


@register.inclusion_tag('blog/includes/partial_post_list.html')
def format_post_list(post_list):
    return {'post_list': post_list}