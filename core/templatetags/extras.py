from django import template

register = template.Library()


@register.filter
def split(value, sep=';'):
    if value is None:
        return []
    return [v for v in str(value).split(sep)]


@register.filter
def get_item(mapping, key):
    try:
        return mapping.get(key)
    except Exception:
        return None


@register.filter
def trim(value):
    if value is None:
        return ''
    return str(value).strip()
