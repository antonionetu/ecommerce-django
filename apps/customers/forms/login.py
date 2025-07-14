from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from apps.orders.models import Cart


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=150)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    cart_reference = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("O campo de usuário não pode estar vazio.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("O campo de senha não pode estar vazio.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Usuário ou senha inválidos.")
            self._user = user
        return cleaned_data

    def save(self):
        ref = self.cleaned_data['cart_reference']
        cart_reference = ref if ref != "vazio" else None

        if cart_reference and not self._user.is_superuser:
            cart = Cart.objects.get(reference__code=cart_reference)
            cart.customer = self._user.customer
            cart.save()

        return self._user
