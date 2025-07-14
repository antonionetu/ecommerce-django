import os, json, time
from requests import request
from dotenv import load_dotenv

from django.shortcuts import redirect


load_dotenv()


class CreatePixPaymentAbacatePay:
    def __init__(self):
        self.url = f'{os.getenv("ABACATE_PAY_API_URL")}/pixQrCode/create'
        self.headers = {
            "Authorization": f'Bearer {os.getenv("ABACATE_PAY_API_KEY")}',
            "Content-Type": "application/json"
        }

    def service(self, customer, order):
        payload = self.format_payload(customer, order)
        response = request("POST", self.url, json=payload, headers=self.headers)

        if response.status_code != 200:
            return {
                'error': 'Não foi possível concluir seu pagamento.'
            }
        
        response = json.loads(response.content.decode('utf-8'))

        return {
            'id': response['data']['id'],
            'key': response['data']['brCode'],
            'qr_code': response['data']['brCodeBase64'],
        }
    
    def polling(self, order, payment_id, timeout=(60*3)+5, interval=5):
        elapsed = 0

        while elapsed < timeout:
            status = self.check_status(payment_id)

            if status.get('status') == 'PAID':
                order.confirm_payment()
                return status
            
            time.sleep(interval)
            elapsed += interval

        return {'status': 'TIMEOUT', 'message': 'Pagamento não confirmado a tempo.'}

    
    def check_status(self, payment_id):
        url = f'{os.getenv("ABACATE_PAY_API_URL")}/pixQrCode/check'
        querystring = { "id": payment_id }
        response = request("GET", url, headers=self.headers, params=querystring)

        if response.status_code != 200:
            return {
                'error': 'Não foi possível verificar o status do pagamento.'
            }

        response = json.loads(response.content.decode('utf-8'))
        return {
            'status': response['data']['status'],
            'data': response['data']
        }

    def format_payload(self, customer, order):
        return {
            "amount": float(order.total_amount()) * 100,
            "expiresIn": 60 * (3 + 1),
            "customer": {
                "name": customer.name,
                "cellphone": customer.phone,
                "email": customer.email,
                "taxId": self.format_cpf(customer.cpf)
            }
        }

    @staticmethod
    def format_cpf(cpf):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    

pix_payment = CreatePixPaymentAbacatePay()
