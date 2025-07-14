from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Customer, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    can_delete = True


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm

    search_fields = [
        'name',
        'cpf',
        'email',
        'phone',
        'user__username',
        'addresses__street',
        'addresses__city',
        'addresses__state',
        'addresses__postal_code',
    ]

    list_display = ('name', 'get_main_postal_code', 'cpf', 'email', 'phone')
    list_filter = ('addresses__city', 'addresses__state')

    inlines = [AddressInline]

    fieldsets = (
        ('Geral', {
            'fields': ('user', 'name', 'email', 'phone', 'cpf'),
        }),
    )

    def get_main_postal_code(self, obj):
        return obj.main_address().postal_code

    get_main_postal_code.short_description = 'CEP'
    get_main_postal_code.admin_order_field = 'addresses'


class UserAdmin(BaseUserAdmin):
    list_display = ('username',)
    list_filter =  ()
    search_fields = [
        'customer__name',
        'customer__cpf',
        'customer__email',
        'customer__phone',
        'username',
        'customer__addresses__street',
        'customer__addresses__city',
        'customer__addresses__state',
        'customer__addresses__postal_code',
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )


admin.site.site_header = "Administração Sasori Imports"
admin.site.site_title = "Administração Sasori Imports"
admin.site.index_title = "Painel de Controle"


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
