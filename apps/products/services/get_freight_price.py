import os, requests

from dotenv import load_dotenv

from django.http import HttpResponse
from django.db.models import F

from ..models import ProductVariant

load_dotenv()


class GetFreightPriceService:
    def __init__(self):
        self.base_url = os.getenv("MELHOR_ENVIO_API_URL").rstrip("/")
        self.freight_price_url = f"{self.base_url}/api/v2/me/shipment/calculate"
        
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv('MELHOR_ENVIO_API_TOKEN')}",
            "Content-Type": "application/json",
            "User-Agent": f"Aplicação {os.getenv('USER_EMAIL')}"
        }

    def service(self, items, to_postal_code):
        payload = self.format_payload(items, to_postal_code)
        response = requests.post(self.freight_price_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()

        return HttpResponse(status=400, message="Ocorreu um erro inesperado ao simular o seu frete.")

    @staticmethod
    def format_payload(items, to_postal_code):
        products = []
        for item in items:
            products.append({
                'variant': ProductVariant.objects.get(id=item['variant_id']),
                'quantity': item['quantity'],
            })

        return {
            "from": { "postal_code": os.getenv('FROM_POSTAL_CODE') },
            "to": { "postal_code": to_postal_code },
            "products": [{
                    "weight": float(item['variant'].weight),
                    "width": float(item['variant'].width),
                    "height": float(item['variant'].height),
                    "length": float(item['variant'].length),
                    "insurance_value": float(item['variant'].price),
                    "quantity": item['quantity']
                } for item in products
            ]
        }


get_freight_price = GetFreightPriceService()
