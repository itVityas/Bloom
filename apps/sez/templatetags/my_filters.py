from django import template


register = template.Library()


@register.filter
def multiply(value, arg):
    return round(float(value) * float(arg), 3)
