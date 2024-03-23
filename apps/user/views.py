from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    UserInformationUpdateForm,
    UserAddressForm,
    UserChangePasswordForm,
)
from apps.user.models import Address
from apps.order.models import Order, OrderBook
from apps.product.models import Book
from django.db.models import Prefetch

class LoginView(UserPassesTestMixin, TemplateView):
    template_name = "user/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (next:=self.request.GET.get("next", None)):
            context["next"] = next
        if (next:=self.request.GET.get("signup", None)):
            context["signup"] = True
        if (next:=self.request.GET.get("changepass", None)):
            context["changepass"] = True
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
        context["form_changepass"] = UserChangePasswordForm()
        context["form_address"] = UserAddressForm()
        context["orders"] = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("orderbook_set", queryset=OrderBook.objects.select_related("book"))
        )
        context["likes"] = self.request.user.user_likes.all()
        context["saves"] = self.request.user.user_saves.all()
        return context
