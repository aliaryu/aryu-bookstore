from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    UserInformationUpdateForm,
    UserAddressForm,
)
from apps.user.models import Address

class LoginView(UserPassesTestMixin, TemplateView):
    template_name = "user/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (next:=self.request.GET.get("next", None)):
            context["next"] = next
        if (next:=self.request.GET.get("signup", None)):
            context["signup"] = True
        return context

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('home:home')


class SignUpView(UserPassesTestMixin, TemplateView):
    template_name = "user/signup.html"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('home:home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "user/profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form_info"] = UserInformationUpdateForm(instance=self.request.user)
        context["addresses"] = Address.objects.filter(user=self.request.user)
        context["form_address"] = UserAddressForm()
        return context

