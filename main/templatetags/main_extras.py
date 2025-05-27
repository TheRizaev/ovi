from django import template
from django.utils.safestring import mark_safe
from main.models import NewsCategory, Partner

register = template.Library()

@register.inclusion_tag('partials/navigation.html', takes_context=True)
def navigation(context):
    """Включает навигационное меню"""
    return {
        'request': context['request']
    }

@register.inclusion_tag('partials/footer.html')
def footer():
    """Включает подвал сайта"""
    return {}

@register.simple_tag
def get_news_categories():
    """Возвращает все категории новостей"""
    return NewsCategory.objects.all()

@register.simple_tag
def get_partner_categories():
    """Возвращает уникальные категории партнеров"""
    categories = Partner.objects.values_list('category', flat=True).distinct()
    category_choices = dict(Partner.PARTNER_TYPES)
    return [(cat, category_choices.get(cat, cat)) for cat in categories]

@register.filter
def multiply(value, arg):
    """Умножает значение на аргумент"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def services_list(value):
    """Преобразует строку услуг в HTML список"""
    if not value:
        return ''
    
    services = value.strip().split('\n')
    html_list = '<ul class="partner-services">'
    for service in services:
        if service.strip():
            html_list += f'<li>{service.strip()}</li>'
    html_list += '</ul>'
    return mark_safe(html_list)

@register.simple_tag(takes_context=True)
def is_active_url(context, url_name):
    """Проверяет, является ли URL активным"""
    request = context['request']
    try:
        return 'active' if request.resolver_match.url_name == url_name else ''
    except AttributeError:
        return ''

@register.filter
def truncate_words_html(value, arg):
    """Обрезает HTML текст до указанного количества слов"""
    from django.utils.html import strip_tags
    from django.template.defaultfilters import truncatewords
    
    # Убираем HTML теги и обрезаем
    plain_text = strip_tags(value)
    return truncatewords(plain_text, arg)

# Добавляем недостающие фильтры
@register.filter
def split(value, separator=','):
    """Разделяет строку по разделителю"""
    if isinstance(value, str):
        return value.split(separator)
    return []

@register.filter
def make_list(value):
    """Превращает строку в список символов"""
    return list(str(value))

@register.filter
def slice_filter(value, arg):
    """Обрезает строку или список"""
    try:
        if ':' in arg:
            start, end = arg.split(':')
            start = int(start) if start else None
            end = int(end) if end else None
            return value[start:end]
        else:
            return value[:int(arg)]
    except (ValueError, TypeError):
        return value