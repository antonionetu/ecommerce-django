from django.http import JsonResponse
from django.shortcuts import render

from .. import services
from .. import forms


def payment(request, ref):
    return strategy(request, ref)


def strategy(request, ref):
    factory = Factory(request, ref)
    factory.context['order'] = factory.order

    if factory.request.method == "GET":
        if factory.pix_payment_id:
            factory.get_pix_check_payment()
            return JsonResponse(factory.context['pix'], safe=False)

        elif factory.payment_method == "pix":
            factory.get_pix_payment_method()

        elif factory.payment_method == "credit_card":
            factory.get_credit_card_payment_method()

    elif factory.request.method == "POST":
        if factory.payment_method == "credit_card":
            factory.post_credit_card_payment_method()

    form = factory.context.get('credit_card_form')
    if form and form.is_valid():
        return JsonResponse({ 'success': True }, satus=200)

    return render(factory.request, factory.template, factory.context) 


class Factory:
    def __init__(self, request, ref):
        self.context = {}
        self.template = 'pages/orders/payment.html'

        self.request = request
        self.ref = ref

        self.customer = self.request.user.customer
        self.order = services.get_order.service(self.request, self.ref)

        self.pix_payment_id = request.GET.get('pix_payment_id')
        self.payment_method = request.GET.get('payment_method')

    def get_pix_payment_method(self):
        self.context['pix'] = services.pix_payment.service(self.customer, self.order)

    def get_pix_check_payment(self):
        self.context['pix'] = services.pix_payment.polling(self.order, self.pix_payment_id)

    def get_credit_card_payment_method(self):
        self.context['credit_card_form'] = forms.CreditCardPaymentForm()

    def post_credit_card_payment_method(self):
        self.context['credit_card_form'] = forms.CreditCardPaymentForm(self.request.POST)
