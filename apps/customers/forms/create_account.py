import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from ..models import BRAZILIAN_STATES, Customer, Address
from apps.orders.models import Cart


class CreateAccountForm(UserCreationForm):
    username = forms.CharField(
        label="Usuário",
        error_messages={'required': 'Por favor, escolha um nome de usuário.'}
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput,
        error_messages={'required': 'Digite uma senha.'}
    )

    password2 = forms.CharField(
        label="Confirmar Senha",
        strip=False,
        widget=forms.PasswordInput,
        error_messages={'required': 'Confirme sua a senha.'}
    )

    email = forms.EmailField(
        required=True,
        label="E-mail",
        error_messages={'required': 'Informe um e-mail válido.'}
    )

    name = forms.CharField(
        max_length=255,
        label="Nome Completo",
        error_messages={'required': 'Por favor, informe seu nome.'}
    )

    phone = forms.CharField(
        max_length=20,
        label="Telefone",
        error_messages={'required': 'Por favor, informe seu telefone.'}
    )

    cpf = forms.CharField(
        max_length=14,
        label="CPF",
        error_messages={'required': 'Por favor, informe seu CPF.'}
    )

    postal_code = forms.CharField(
        max_length=20,
        label="CEP",
        error_messages={'required': 'Informe o CEP.'}
    )

    street = forms.CharField(
        max_length=255,
        label="Rua",
        error_messages={'required': 'Informe a rua.'}
    )

    number = forms.CharField(
        max_length=10,
        label="Número",
        error_messages={'required': 'Informe o número.'}
    )

    complement = forms.CharField(
        max_length=100,
        label="Complemento",
        error_messages={'required': 'Informe o complemento.'}
    )

    neighborhood = forms.CharField(
        max_length=100,
        label="Bairro",
        error_messages={'required': 'Informe o bairro.'}
    )

    city = forms.CharField(
        max_length=100,
        label="Cidade",
        error_messages={'required': 'Informe a cidade.'}
    )

    state = forms.ChoiceField(
        choices=BRAZILIAN_STATES,
        label="Estado",
        error_messages={'required': 'Selecione o estado.'}
    )

    country = forms.CharField(
        max_length=100,
        initial="Brasil",
        label="País",
        disabled=True,
        required=False
    )

    cart_reference = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2", "name", "phone", "cpf",
            "street", "number", "complement", "neighborhood", "city", "state",
            "postal_code", "country"
        )

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        if cpf:
            cpf_digits = re.sub(r'\D', '', cpf)
            if len(cpf_digits) != 11:
                raise forms.ValidationError("CPF deve conter 11 dígitos.")
            return cpf_digits
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            digits = re.sub(r'\D', '', phone)
            if not digits:
                raise forms.ValidationError("Telefone inválido.")
            return digits
        return phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code")
        if postal_code:
            digits = re.sub(r'\D', '', postal_code)
            if len(digits) != 8:
                raise forms.ValidationError("CEP inválido. Formato esperado: 00000-000")
            return digits
        return postal_code

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name or not name.strip():
            raise forms.ValidationError("O nome não pode estar vazio.")
        
        def capitalize_word(word):
            return word.capitalize() if len(word) >= 3 else word

        words = name.strip().split()
        capitalized_words = [capitalize_word(w) for w in words]
        return ' '.join(capitalized_words)

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        customer = Customer.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            cpf=self.cleaned_data['cpf']
        )

        Address.objects.create(
            customer=customer,
            is_main=True,
            street=self.cleaned_data['street'],
            number=self.cleaned_data['number'],
            complement=self.cleaned_data['complement'],
            neighborhood=self.cleaned_data['neighborhood'],
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            postal_code=self.cleaned_data['postal_code'],
            country=self.cleaned_data['country']
        )

        ref = self.cleaned_data['cart_reference']
        cart_reference = ref if ref != "vazio" else None

        if cart_reference:
            cart = Cart.objects.get(reference__code=cart_reference)
            cart.customer = customer
            cart.save()

        return user, cart_reference
