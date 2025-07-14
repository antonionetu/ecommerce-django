from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext

from ..models import Product, ProductImage


class ProductImageAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = (
            "images",
        )

    images = forms.FileField(
        widget=forms.ClearableFileInput(),
        label=gettext("Add images"),
        required=False,
    )

    def clean_image(self):
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_images(self, product):
        for upload in self.files.getlist("images"):
            image = ProductImage(product=product, image=upload)
            image.save()
