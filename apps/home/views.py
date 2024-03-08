from django.shortcuts import render
from django.views.generic import TemplateView
from apps.product.models import Book, Author, Tag
from django.db.models import Count


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_books"] = Book.objects.select_related("discount").annotate(likes_count=Count('likes')).order_by("-likes_count", "-id")[:10]
        context["authors"] = Author.objects.order_by("-id")[:50]
        context["newest_books"] = Book.objects.select_related("discount").order_by("-id", "-id")[:10]
        context["tags"] = Tag.objects.order_by("-id")[:50]

        return context