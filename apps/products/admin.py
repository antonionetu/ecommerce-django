from .models import Product, ProductVariant, ProductImage, ProductReview, Category

from django.contrib import admin


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['name', 'created_at']
    list_filter = ['category']
    inlines = [ProductVariantInline, ProductImageInline]
    fieldsets = (
        ('Geral', {
            'fields': ('name', 'description', 'category'),
        }),
    )


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'customer__name']
    list_display = ['product', 'customer', 'rating', 'created_at']
    list_filter = ['rating']


admin.site.register(Category)
