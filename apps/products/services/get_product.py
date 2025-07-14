from django.shortcuts import get_object_or_404

from ..models import Product


class GetProductService:
    @staticmethod
    def service(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return product

    def service_proxy(self, request, product_id):
        data = self.service(request, product_id)
        return data


get_product = GetProductService()
