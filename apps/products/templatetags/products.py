from django import template

register = template.Library()


@register.filter
def has_stock(product):
    return product.variants.filter(stock__gt=0).exists()
