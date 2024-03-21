from django.views.generic import (
    DetailView,
    ListView
)
from apps.product.models import (
    Book,
    Author,
    Category,
    Genre,
    Tag
)
from apps.comment.models import Comment
from django.db.models import Prefetch, Q
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


class GenreListView(ListView):
    model = Genre
    template_name = "list.html"
    context_object_name = "books"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get("pk")).first().book_set.all().select_related("discount")
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        title = get_object_or_404(Genre, pk=self.kwargs.get("pk")).genre_name
        context["title"] = f"ژانر: {title}"
        return context


class TagListView(ListView):
    model = Tag
    template_name = "list.html"
    context_object_name = "books"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get("pk")).first().book_set.all().select_related("discount")
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        title = get_object_or_404(Tag, pk=self.kwargs.get("pk")).tag_name
        context["title"] = f"تگ: {title}"
        return context


class AllBooksListView(ListView):
    model = Book
    template_name = "list.html"
    context_object_name = "books"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("discount").order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = f"همه کتاب ها"
        return context


class DiscountBooksListView(ListView):
    model = Book
    template_name = "list.html"
    context_object_name = "books"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(discount__isnull=False).select_related("discount").order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = f"تخفیف دار ها"
        return context


class SearchListView(ListView):
    model = Book
    template_name = "list.html"
    context_object_name = "books"
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query is not None:
            search_query = search_query.strip()
        if search_query:
            if "ژانر" in search_query:
                search_query= search_query.replace("ژانر", "").strip()
                queryset = queryset.filter(
                    genre__genre_name__icontains=search_query
                ).select_related("discount").order_by("-id").distinct()
            elif "#" in search_query:
                search_query= search_query.replace("#", "").strip()
                queryset = queryset.filter(
                    tag__tag_name__icontains=search_query
                ).select_related("discount").order_by("-id").distinct()
            else:
                queryset = queryset.filter(
                    Q(book_name__icontains=search_query) |
                    Q(category__cat_name__icontains=search_query)
                ).select_related("discount").order_by("-id").distinct()
        return queryset.select_related("discount")

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["title"] = f"نتایج جستـــ و جو"
        return context
