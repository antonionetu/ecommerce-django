from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .. import forms

class LoginService:
    @staticmethod
    def service(request):
        if request.user.is_authenticated:
            return redirect("products")

        if request.method == "POST":
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)

                if user.is_superuser:
                    return HttpResponseRedirect('/admin/')

                return redirect("products")

        else:
            form = forms.LoginForm()

        return form

