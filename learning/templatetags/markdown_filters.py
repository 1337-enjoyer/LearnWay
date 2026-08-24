from django import template
from django.template.defaultfilters import stringfilter
import markdown
# from markdown.extensions import fenced_code

register = template.Library()


@register.filter(name='markdown')
@stringfilter
def markdown_filter(value):
    # extensions=['fenced_code'] нужен, чтобы Markdown понимал блоки кода с ``` [citation:2][citation:8]
    return markdown.markdown(value, extensions=['fenced_code', 'codehilite'])
