from django.views.generic import TemplateView
from apps.product.models import Book
import json


class CartView(TemplateView):
    template_name = "order/cart.html"

    def get_cookie_cart(self):
        if (cart:=self.request.COOKIES.get("cart")):
            return json.loads(cart)
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = []

        cart = self.get_cookie_cart()
        if cart:
            books = Book.objects.filter(id__in=cart.keys())
            for book in books:
                context["books"].append((book, cart[str(book.id)]))

        return context
