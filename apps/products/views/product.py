import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .. import services
from ..models import Product


def product(request, product_id):
    return strategy(request, product_id)


def strategy(request, product_id):
    factory = Factory(request, product_id)
    factory.context['product'] = factory.product

    if factory.request.GET.get('CEP'):
        factory.get_freight_price()
        return JsonResponse(factory.context.get('freight_prices'), safe=False)

    return render(factory.request, factory.template, factory.context)


class Factory:
    def __init__(self, request, product_id):
        self.context = {}
        self.template = 'pages/products/product.html'

        self.request = request
        self.product = services.get_product.service(request, product_id)
        self.content_type = request.headers.get('Content-Type')

    def get_freight_price(self):
        self.context['freight_prices'] = services.get_freight_price.service(
            [{
                "variant_id":self.product.variants.first().id,
                "quantity": 1
            }], self.request.GET.get('CEP')
        )
