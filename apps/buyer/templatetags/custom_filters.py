from django.template import Library

register = Library()

@register.filter
def times(number):
    return range(number)

