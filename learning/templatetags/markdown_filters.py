from django import template
from django.template.defaultfilters import stringfilter
import markdown
from markdown.extensions import fenced_code, codehilite, tables, toc

register = template.Library()


@register.filter(name='markdown')
@stringfilter
def markdown_filter(value):
    """
    Преобразует Markdown в HTML с поддержкой:
    - подсветки кода (fenced_code)
    - таблиц (tables)
    - оглавления (toc)
    """
    if not value:
        return ''

    return markdown.markdown(
        value,
        extensions=[
            'fenced_code',      # Блоки кода с ```python
            'codehilite',       # Подсветка синтаксиса
            'tables',           # Таблицы
            'toc',              # Оглавление (опционально)
            'nl2br',            # Переносы строк
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'codehilite',
            }
        }
    )
