from django.db import models
from django.contrib.auth.models import User


BRAZILIAN_STATES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(null=True, blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name="CPF")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def main_address(self):
        return self.addresses.filter(is_main=True).first()

    def set_main_address(self, new_main_address):
        old_address = self.addresses.filter(is_main=True).first()
        old_address.is_main = False
        old_address.save()
        new_main_address.is_main = True

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name


class Address(models.Model):
    customer = models.ForeignKey(Customer, related_name="addresses", on_delete=models.CASCADE, verbose_name="Cliente")
    is_main = models.BooleanField(default=False, verbose_name="Endereço Principal")
    street = models.CharField(max_length=255, verbose_name="Rua")
    number = models.CharField(max_length=10, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, choices=BRAZILIAN_STATES, verbose_name="Estado")
    postal_code = models.CharField(max_length=20, verbose_name="CEP")
    country = models.CharField(max_length=100, default="Brasil", verbose_name="País")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}, {self.state}"
