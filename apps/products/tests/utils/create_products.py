import os, random
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


from apps.products.models import Category, Product

def generate_image_file(name='image.jpg', size=(300, 300), color=(255, 0, 0)):
    image = Image.new('RGB', size, color)
    buffer = BytesIO()    
    image.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue(), name)

def create_products():
    categories = ['T-Shirts', 'Jeans', 'Hoodies', 'Jackets', 'Shoes', 'Accessories']
    category_objs = []

    for cat_name in categories:
        obj, _ = Category.objects.get_or_create(name=cat_name)
        category_objs.append(obj)

    for i in range(40):
        product = Product.objects.create(
            name=f"Product {i + 1}",
            price=round(random.uniform(20, 300), 2),
            description="Stylish and comfortable.",
            image=generate_image_file(name=f'product_{i + 1}.jpg')
        )
        product.category.set(random.sample(category_objs, random.randint(1, 3)))
