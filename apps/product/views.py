from django.views.generic import DetailView
from apps.product.models import Book
from apps.comment.models import Comment
from django.db.models import Prefetch


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
        Prefetch("comments", queryset=Comment.objects.filter(approve=True).select_related("user"))
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context