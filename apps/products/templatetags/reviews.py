from django import template

register = template.Library()


@register.simple_tag
def star_rating(rating, out_of=5):
    filled = '★' * int(rating)
    empty = '☆' * (out_of - int(rating))
    return filled + empty
