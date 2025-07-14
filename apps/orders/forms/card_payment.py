from django import forms


class CreditCardPaymentForm(forms.Form):
    cardholderName = forms.CharField(
        label="Nome do Titular",
        max_length=255,
        widget=forms.TextInput(attrs={"id": "cardholderName"})
    )

    cardNumber = forms.CharField(
        label="Número do Cartão",
        max_length=20,
        widget=forms.TextInput(attrs={"id": "cardNumber"})
    )

    expirationDate = forms.CharField(
        label="Data de Expiração (MM/AA)",
        max_length=7,
        widget=forms.TextInput(attrs={"id": "expirationDate"})
    )

    securityCode = forms.CharField(
        label="Código de Segurança",
        max_length=4,
        widget=forms.TextInput(attrs={"id": "securityCode"})
    )

    installments = forms.IntegerField(
        label="Parcelas",
        widget=forms.Select(attrs={"id": "installments"})
    )

    card_token = forms.CharField(
        widget=forms.HiddenInput(attrs={"id": "card_token"})
    )
