from django.views.generic import DetailView
from apps.product.models import Book


class BookDetailView(DetailView):
    template_name = "product/book.html"
    context_object_name = "book"
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context