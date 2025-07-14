from django.http import HttpResponse
from django.shortcuts import render

from .. import services


def sign_in(request):
    return strategy(request)


def strategy(request):
    if request.method in ("GET", "POST"):
        context, template = factory(request)

        if not hasattr(context.get("form"), "is_valid"):
            return context["form"]

        return render(request, template, context)

    return HttpResponse(status=405)


def factory(request):
    context = {
        "form": services.login.service(request),
    }

    return context, "pages/customers/auth/sign_in.html"
