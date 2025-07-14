from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import reverse

from .. import forms

class CreateAccountService:
    @staticmethod
    def service(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("products"))

        if request.method == "POST":
            form = forms.CreateAccountForm(request.POST)
            if form.is_valid():
                user, cart_reference = form.save()
                login(request, user)

                if cart_reference:
                    return HttpResponseRedirect(reverse("orders_cart", kwargs={"ref": cart_reference}))

                return HttpResponseRedirect(reverse("products"))

        else:
            form = forms.CreateAccountForm()

        return form


create_account = CreateAccountService()
