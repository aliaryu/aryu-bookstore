from django.views.generic import (
    DetailView,
    ListView
)
from apps.product.models import (
    Book,
    Author,
    Category
)
from apps.comment.models import Comment
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404


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
    queryset = Author.objects.prefetch_related(
        Prefetch("author_books", queryset=Book.objects.only("book_name")),
        Prefetch("translator_books", queryset=Book.objects.only("book_name")),
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


class CategoryListView(ListView):
    model = Book
    template_name = "list.html"
    context_object_name = "books"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get("pk")).select_related("discount")
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        title = get_object_or_404(Category, pk=self.kwargs.get("pk")).cat_name
        context["title"] = f"دسته بندی: {title}"
        return context
