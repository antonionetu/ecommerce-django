import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

from .. import services
from apps.products import services as product_services
from apps.orders import forms as order_forms


def cart(request, ref):
    return strategy(request, ref)


def strategy(request, ref):
    factory = Factory(request, ref)

    if factory.request.method == "GET":
        factory.get()

        if not factory.context['cart'] and ref != 'vazio':
            return HttpResponseRedirect(reverse('orders_cart',
                kwargs={'ref': 'vazio'}
            ))

    elif factory.request.method == "POST":
        factory.post()

    elif factory.request.method == "PATCH":
        factory.patch()

    elif factory.request.method == "DELETE":
        factory.delete()

    else:
        return HttpResponse(status=405)

    form = factory.context.get('form')

    if not form and factory.request.method != "GET":
        return JsonResponse(factory.context)

    elif form and form.is_valid():
        return HttpResponseRedirect(reverse(
            'orders_payment', kwargs={'ref': ref}
        ))

    return render(factory.request, factory.template, factory.context) 


class Factory:
    def __init__(self, request, ref):
        self.context = {}
        self.template = 'pages/orders/cart.html'

        self.request = request
        self.ref = ref

    def _freight_price(self):
        return json.dumps(
            product_services.get_freight_price.service(
                [{
                    'variant_id':item.product_variant.id,
                    'quantity':item.quantity
                } for item in self.context['cart'].items.all()],
                self.request.user.customer.main_address().postal_code
            )
        )

    def get(self):
        self.context['cart'] = services.get_cart.service(self.request, self.ref)
        if self.request.user.is_authenticated and self.context['cart']:
            self.context['form'] = order_forms.CreateOrderForm()
            self.context ['freights'] = self._freight_price()
    
    def post(self):
        form = order_forms.CreateOrderForm(self.request.POST)
        if form.is_valid():
            form.save()
        self.context['form'] = form

    def patch(self):
        self.context['add_items'] = services.add_products_to_cart.service(self.request, self.ref)

    def delete(self):
        self.context['remove_items'] = services.remove_product_from_cart.service(self.request, self.ref)
