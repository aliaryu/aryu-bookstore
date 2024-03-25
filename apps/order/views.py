from django.views.generic import TemplateView
from apps.product.models import Book
from .forms import PaymentForm
from django.shortcuts import render
import json


class CartView(TemplateView):
    template_name = "order/cart.html"
    form_class = PaymentForm

    def get_cookie_cart(self):
        if (cart:=self.request.COOKIES.get("cart")):
            return json.loads(cart)
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment_form"] = self.form_class(self.request.user)
        context["books"] = []
        cart = self.get_cookie_cart()
        if cart:
            books = Book.objects.filter(id__in=cart.keys()).select_related("discount").prefetch_related("author")
            for book in books:
                context["books"].append((book, cart[str(book.id)]))

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            user = request.user, 
            cookie = self.get_cookie_cart(),
            data = request.POST
        )

        context = self.get_context_data()

        if form.is_valid():
            context["payment_form"] = self.form_class(self.request.user)
            context["payment_success"] = True
            response = render(request, self.template_name, context)
            response.delete_cookie("cart")
            return response
        else:
            context['payment_form'] = form
            return render(request, self.template_name, context)
