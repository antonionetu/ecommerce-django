from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('carrinho/<slug:ref>/', views.cart, name="orders_cart"),
    path('carrinho/<slug:ref>/pagamento', views.payment, name="orders_payment"),
]
