from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .. import services


def products(request):
    return strategy(request)


def strategy(request):
    context, template = factory(request)

    if not context['products']:
        return HttpResponse(status=404)

    if request.GET.get('p') or request.GET.get('q'):
        _products = list(context['products'].values()) 
        return JsonResponse(_products, safe=False, status=200)
    
    return render(request, template, context)


def factory(request):
    data = {
        'products': services.product_list.service(request, page=request.GET.get('p', 1))
    }

    return data, 'pages/products/home.html'
    