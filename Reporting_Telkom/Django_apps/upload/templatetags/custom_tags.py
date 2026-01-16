from django import template

register = template.Library()

# Filter untuk mengambil value dari dictionary (Dipakai di baris data)
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Filter untuk menghapus underscore di Header (Dipakai di nama kolom)
@register.filter
def replace_underscore(value):
    if isinstance(value, str):
        return value.replace('_', ' ')
    return value