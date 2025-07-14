from ..models import Cart


class GetCart:
    def service(self, request, ref):
        cart = Cart.objects.filter(reference__code=ref, shopping=True).first()
        return cart
    
    
get_cart = GetCart()
