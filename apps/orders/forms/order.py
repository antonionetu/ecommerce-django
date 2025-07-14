from django import forms
from django.core.exceptions import ValidationError

from apps.products import services as product_services

from ..models import Cart, Order


class CreateOrderForm(forms.Form):
    cart_reference = forms.CharField(max_length=100)
    freight_id = forms.CharField(max_length=100)

    def clean_cart_reference(self):
        ref = self.cleaned_data.get('cart_reference')

        try:
            cart = Cart.objects.get(reference__code=ref)
        except Cart.DoesNotExist:
            raise ValidationError("Carrinho não encontrado.")

        return cart

    def clean_freight_id(self):
        id = self.cleaned_data.get('freight_id')
        cart = self.cleaned_data.get('cart_reference')

        freights = product_services.get_freight_price.service(
            [{
                'variant_id': item.product_variant.id,
                'quantity': item.quantity
            } for item in cart.items.all()],
            cart.customer.main_address().postal_code
        )

        return next((f for f in freights if f.get('id') == int(id)), None)

    def save(self):
        cart = self.cleaned_data.get('cart_reference')
        freight = self.cleaned_data.get('freight_id')

        try:
            order = Order.objects.get(cart=cart)
            order.purchase_amount = cart.subtotal()
            order.freight_business = freight.get('name')
            order.freight_amount = freight.get('price')
            order.save()

        except:
            Order.objects.create(
                cart=cart, 
                purchase_amount=cart.subtotal(), 
                freight_amount=freight.get('price')
            )
        
