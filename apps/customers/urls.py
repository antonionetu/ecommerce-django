from django.urls import path

from . import views


urlpatterns = [
    path('autenticacao/entrar/', views.sign_in, name="customers_sign_in"),
    path('autenticacao/cadastrar/', views.sign_up, name="customers_sign_up"),
]
