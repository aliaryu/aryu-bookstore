from django.views.generic import TemplateView


class CartView(TemplateView):
    template_name = "order/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
