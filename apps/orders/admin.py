from django.contrib import admin
from .models import Cart, CartItem, CartReference, Order

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartReferenceInline(admin.StackedInline):
    model = CartReference
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['display_customer', 'display_reference_code', 'shopping']
    inlines = [CartItemInline, CartReferenceInline]
    fieldsets = (
        ('Geral', {
            'fields': ('customer', 'shopping'),
        }),
    )

    def display_customer(self, obj):
        return obj.customer if obj.customer else "Ainda não cadastrado"
    display_customer.short_description = 'Cliente'

    def display_reference_code(self, obj):
        if hasattr(obj, 'reference') and obj.reference:
            return obj.reference.code
        return "-"
    display_reference_code.short_description = 'Código de Referência'

    def display_customer(self, obj):
        if obj.customer:
            return obj.customer
        return "Ainda não cadastrado"
    display_customer.short_description = 'Cliente'
    display_customer.admin_order_field = 'customer__name'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cart', 'purchase_amount', 'freight_amount', 'display_total', 'paid', 'created_at']

    def display_total(self, obj):
        return obj.total_amount()
    display_total.short_description = 'Total'
    display_total.admin_order_field = 'total_amount'

