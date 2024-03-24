from django.views.generic import TemplateView, FormView
from apps.product.models import Book
from .forms import PaymentForm
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
