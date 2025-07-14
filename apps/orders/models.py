import uuid

from django.db import models
from django.core.exceptions import ValidationError

import emails as send_email

from apps.customers.models import Customer
from apps.products.models import ProductVariant


class CartReference(models.Model):
    code = models.SlugField(verbose_name="Código", unique=True, null=False)
    cart = models.OneToOneField('Cart', related_name='reference', on_delete=models.CASCADE, verbose_name="Carrinho")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def generate_unique_code(self, attempts=0):
        if attempts >= 3:
            raise ValidationError("Não foi possível gerar um código único após 3 tentativas.")

        candidate = uuid.uuid4().hex
        if CartReference.objects.filter(code=candidate).exists():
            return self.generate_unique_code(attempts + 1)
        return candidate

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Referência"
        verbose_name_plural = "Referências"

    def __str__(self):
        return f"Código de Referência: {self.code}"


class CartItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name="Variante do Produto")
    cart = models.ForeignKey('Cart', related_name='items', on_delete=models.CASCADE, verbose_name="Carrinho")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade")

    def subtotal(self):
        return self.product_variant.price * self.quantity

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, related_name="cart", null=True, on_delete=models.SET_NULL, verbose_name="Cliente")
    shopping = models.BooleanField(default=True, verbose_name="Ainda comprando")

    def subtotal(self):
        return sum(p.subtotal() for p in self.items.all())

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    def __str__(self):
        return f"{self.customer.name if self.customer else 'unknown so far'} - {'Shopping' if self.shopping else 'Done'}"


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name="Carrinho")
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da compra")
    freight_business = models.TextField(verbose_name="Empresa do frete")
    freight_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do frete")
    paid = models.BooleanField(default=False, verbose_name="Pago")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def total_amount(self):
        return self.purchase_amount + self.freight_amount
    
    def confirm_payment(self):
        self.paid = True
        self.save()
        self.cart.shopping = False
        self.cart.save()
        send_email.admins.new_order(self)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"{self.cart.customer.name} - {self.created_at}"


class Token(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    value = models.CharField(max_length=255, verbose_name="Valor")

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
