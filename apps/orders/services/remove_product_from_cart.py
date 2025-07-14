import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from apps.products.models import ProductVariant
from ..models import CartReference, CartItem


class RemoveProductsFromCartService:
    @staticmethod
    def service(request, reference_code):
        request_data = json.loads(request.body)

        product_variant = get_object_or_404(ProductVariant, id=request_data.get("product_variant_id"))
        cart_reference = get_object_or_404(CartReference, code=reference_code)
        cart_item = CartItem.objects.get(cart__reference=cart_reference, product_variant=product_variant)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        elif cart_item.quantity == 1:
            cart_item.delete()


remove_product_from_cart = RemoveProductsFromCartService()
