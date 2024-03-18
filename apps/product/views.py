from django.views.generic import DetailView
from apps.product.models import Book, Author
from apps.comment.models import Comment
from django.db.models import Prefetch


class BookDetailView(DetailView):
    template_name = "product/book.html"
    context_object_name = "book"

    # NEEDS DEFER & ONLY
    queryset = Book.objects.select_related(
        "category",
        "discount"
    ).prefetch_related(
        "tag",
        "genre",
        "author",
        "translator",
        "likes",
        "saves",
        Prefetch("comments", queryset=Comment.objects.filter(approve=True).select_related("user").defer(
            "user__username",
            "user__password",
            "user__email",
            "user__birth_date",
            "user__is_superuser",
            "user__is_staff",
            "user__is_active",
            "user__is_delete",
            "user__last_login",
            "user__date_joined",
            ))
    )


class AuthorDetailView(DetailView):
    template_name = "product/author.html"
    context_object_name = "author"

    # NEEDS DEFER & ONLY
    queryset = Book.objects.all()
