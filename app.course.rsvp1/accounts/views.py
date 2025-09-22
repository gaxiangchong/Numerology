from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form: LoginForm) -> HttpResponse:
        remember_me = form.cleaned_data.get("remember_me")
        response = super().form_valid(form)
        if remember_me:
            # One month session
            self.request.session.set_expiry(60 * 60 * 24 * 30)
        else:
            self.request.session.set_expiry(0)  # browser session
        return response


class RegisterView(View):
    template_name = "accounts/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy("events:list"))
        return render(request, self.template_name, {"form": form})


# Create your views here.
