from django.shortcuts import get_object_or_404
from ..models import Order


class GetOrder:
    def service(self, request, ref):
        return get_object_or_404(Order, cart__reference__code=ref)
    
    
get_order = GetOrder()
