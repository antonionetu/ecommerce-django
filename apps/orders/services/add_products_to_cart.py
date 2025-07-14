import json

from django.shortcuts import get_object_or_404

from apps.products.models import ProductVariant
from ..models import CartReference, CartItem, Cart


class AddProductsToCartService:
    @staticmethod
    def service(request, reference_code):
        request_data = json.loads(request.body)

        product_variant = get_object_or_404(ProductVariant, id=request_data.get("product_variant_id"))
        cart_reference = CartReference.objects.filter(code=reference_code).first()

        if not cart_reference:
            cart = Cart.objects.create()

            if request.user.is_authenticated:
                cart.customer = request.user.customer
                cart.save()

            CartItem.objects.create(product_variant=product_variant, cart=cart)
            cart_reference = CartReference.objects.create(cart=cart)
            
            return {
                'cart_reference': cart_reference.code
            }

        cart = Cart.objects.get(reference=cart_reference)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=product_variant)

        if not created:
            cart_item.quantity += 1

        cart_item.save()
        
        return {
            'cart_reference': cart_reference.code
        }


add_products_to_cart = AddProductsToCartService()
