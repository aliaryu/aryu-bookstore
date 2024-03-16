from django.shortcuts import render
from django.views.generic import TemplateView
from apps.product.models import Book, Author, Tag
from apps.order.models import OrderBook
from django.db.models import Count, Sum
import random


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_books"] = sorted(Book.objects.select_related("discount")
            .annotate(likes_count=Count('likes')).order_by("-likes_count", "-id")[:10],
                key=lambda x: random.random())
        
        context["authors"] = sorted(Author.objects.order_by("-id")[:50],
            key=lambda x: random.random())
        
        context["newest_books"] = sorted(Book.objects.select_related("discount")
            .order_by("-id")[:10], key=lambda x: random.random())
        
        context["tags"] = sorted(Tag.objects.order_by("-id")[:50], key=lambda x: random.random())

        context["top_selling"] = sorted(Book.objects.filter(id__in=OrderBook.objects.values('book')
            .annotate(total_sales=Sum('count')).order_by('-total_sales')[:10].values_list('book', 
                flat=True)).select_related("discount").order_by()[:10], key=lambda x: random.random())

        context["discount_books"] = Book.objects.filter(discount__isnull=False).select_related(
            "discount").order_by("?")[:10]

        return context
