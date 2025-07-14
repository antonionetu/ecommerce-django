from django.db.models import Value, F, CharField, Subquery, OuterRef
from django.db.models.functions import Concat

from ..models import Product, ProductImage


class ProductListService:
    @staticmethod
    def service(request, quantity=8, page=1):
        page, quantity = int(page), int(quantity)
        start = (page - 1) * quantity
        end = start + quantity

        products = Product.objects.filter(
            variants__stock__gt=0
        ).annotate(
            url=Concat(
                Value('/produtos/'), F('id'), Value('/'),
                output_field=CharField()
            ),
            first_image_url=Subquery(
                ProductImage.objects.filter(product=OuterRef('pk')).values('image')[:1]
            )
        ).distinct().prefetch_related('images')[start:end]
        
        return products

    def service_proxy(self, request, quantity=8, page=1):
        data = self.service(request, quantity, page)
        return data


product_list = ProductListService()
