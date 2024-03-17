from django.views.generic import DetailView
from apps.product.models import Book


class BookDetailView(DetailView):
    template_name = "product/book.html"
    context_object_name = "book"

    # NEEDS DEFFER & ONLY
    queryset = Book.objects.select_related(
        "category",
        "discount"
    ).prefetch_related(
        "tag",
        "genre",
        "author",
        "translator",
        "comments__user"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context