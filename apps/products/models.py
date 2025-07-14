import uuid

from django.db import models
from apps.customers.models import Customer


class Category(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=100)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=255)
    description = models.TextField(verbose_name="Descrição", blank=True)
    category = models.ManyToManyField(Category, verbose_name="Categorias")
    created_at = models.DateTimeField(verbose_name="Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    SIZE_TYPE_CHOICES = [
        ('clothing', 'Roupas'),
        ('shoes', 'Calçados'),
        ('volume', 'Volume'),
        ('generic', 'Genérico'),
    ]

    product = models.ForeignKey(Product, verbose_name="Produto", related_name='variants', on_delete=models.CASCADE)
    size_type = models.CharField(verbose_name="Tipo", max_length=20, choices=SIZE_TYPE_CHOICES)
    size_label = models.CharField(verbose_name="Etiqueta", max_length=50)
    price = models.DecimalField(verbose_name="Preço", max_digits=8, decimal_places=2)
    weight = models.DecimalField(verbose_name="Peso (kg)", max_digits=6, decimal_places=2, default=1.0)
    width = models.DecimalField(verbose_name="Largura (cm)", max_digits=6, decimal_places=2, default=10.0)
    height = models.DecimalField(verbose_name="Altura (cm)", max_digits=6, decimal_places=2, default=10.0)
    length = models.DecimalField(verbose_name="Comprimento (cm)", max_digits=6, decimal_places=2, default=10.0)
    insurance_value = models.DecimalField(verbose_name="Seguro", max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(verbose_name="Estoque", default=0)

    class Meta:
        verbose_name = "Variante"
        verbose_name_plural = "Variantes"

    def __str__(self):
        return f"{self.product.name} - {self.size_label}"


class ProductImage(models.Model):
    def folder(self, file_name):
        ext = file_name.split('.')[-1]
        product_slug = self.product.name.replace(' ', '-')
        filename = f"{uuid.uuid4()}.{ext}"
        return f'store/products/{product_slug}_{self.product.id}/{filename}'

    product = models.ForeignKey(Product, verbose_name="Produto", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Imagem", upload_to=folder)

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produto", related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, verbose_name="Cliente", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(verbose_name="Avaliação", choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(verbose_name="Comentário", blank=True)
    created_at = models.DateTimeField(verbose_name="Criado em", auto_now_add=True)

    class Meta:
        unique_together = ('product', 'customer')
        ordering = ['-created_at']
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"

    def __str__(self):
        return f"{self.customer.name} - {self.product} ({self.rating} estrelas)"
