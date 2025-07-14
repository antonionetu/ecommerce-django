from django.http import HttpResponse
from django.shortcuts import render

from .. import services


def sign_up(request):
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
        "form": services.create_account.service(request),
    }

    return context, "pages/customers/auth/sign_up.html"
