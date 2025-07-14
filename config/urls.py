from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.static import serve


urlpatterns = [
    path('', RedirectView.as_view(url='/produtos/', permanent=False)),

    path('admin/', admin.site.urls),
    path('produtos/', include('apps.products.urls')),
    path('pedidos/', include('apps.orders.urls')),
    path('clientes/', include('apps.customers.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ]


handler404 = 'config.handlers.http_error_404'
handler500 = 'config.handlers.http_error_500'
