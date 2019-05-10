from django import template
from core.textutils import get_hashtags
from django.utils.safestring import mark_safe
    # https://docs.djangoproject.com/en/2.2/ref/utils/#django.utils.safestring.mark_safe

register = template.Library()
    # https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/


@register.filter
def link_hashtags(value):
    # https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-filters
    hashtags = get_hashtags(value)
    for tag in hashtags:
        value = value.replace(f"#{tag}", f'<a href="?tag={tag}">#{tag}</a>')
    return mark_safe(value)