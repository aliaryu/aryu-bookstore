from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Category,
    Genre,
    Tag,
    Author,
    Book
)
from apps.comment.models import Comment
from django.contrib.contenttypes.admin import GenericStackedInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    ordering = ["cat_name"]
    search_fields = ["cat_name"]
    list_display_links = None
    list_display = ["cat_name", "cat_parent", "edit", "delete"]
    fields = ["cat_name", "cat_parent",]
    readonly_fields = []

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:product_category_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:product_category_delete', args=[obj.id]),
            translate
        )
    
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre
    ordering = ["genre_name"]
    search_fields = ["genre_name"]
    list_display_links = None
    list_display = ["genre_name", "edit", "delete"]
    fields = ["genre_name",]
    readonly_fields = []

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:product_genre_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:product_genre_delete', args=[obj.id]),
            translate
        )

    edit.short_description = _("view/edit")
    delete.short_description = _("delete")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    ordering = ["-id"]
    search_fields = ["tag_name"]
    list_display_links = None
    list_display = ["tag_name", "edit", "delete"]
    fields = ["tag_name"]

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:product_tag_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:product_tag_delete', args=[obj.id]),
            translate
        )

    edit.short_description = _("view/edit")
    delete.short_description = _("delete")


class CommentApprovedInline(GenericStackedInline):
    model = Comment
    extra = 0
    fields = ["user", "text", "answer", "approve", "create_at"]
    readonly_fields = ["create_at"]
    verbose_name = _("comment")
    verbose_name_plural = _("approved comment")
    classes = ('collapse',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(approve=True)
    
    def has_add_permission(self, request, obj=None):
        return False


class CommentNotApprovedInline(GenericStackedInline):
    model = Comment
    extra = 0
    fields = ["user", "text", "answer", "approve", "create_at"]
    readonly_fields = ["create_at"]
    verbose_name = _("comment")
    verbose_name_plural = _("not approved comment")
    classes = ('collapse',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(approve=False)
    
    def has_add_permission(self, request, obj=None):
        return False


class BookInline(admin.StackedInline):
    model = Book.author.through
    extra = 0
    verbose_name = _("book")
    verbose_name_plural = _("books")
    classes = ('collapse',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    inlines = [
        BookInline,
        CommentApprovedInline,
        CommentNotApprovedInline,
    ]
    ordering = ["-id"]
    search_fields = ["full_name", "nationality"]
    list_display_links = None
    list_display = ["full_name", "nationality", "short_biography", "edit", "delete"]
    fields = ["full_name", "nationality", "biography", "brief", "display_image", "image"]
    readonly_fields = ["display_image"]

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:product_author_change', args=[obj.id]),
            translate
        )
    
    def short_biography(self, obj):
        if len(obj.biography) > 50:
            return obj.biography[:50] + " ..."
        else:
            return obj.biography

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:product_author_delete', args=[obj.id]),
            translate
        )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" style="background-color: #121212;"/>'.format(obj.image.url))
        else:
            return _("there is no image")

    short_biography.short_description = _("description")
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
    display_image.short_description = _("preview")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    model = Book
    inlines = [
        CommentApprovedInline,
        CommentNotApprovedInline,
    ]
    ordering = ["-id"]
    search_fields = ["book_name", "publisher", "author__full_name", "translator__full_name"]
    list_display_links = None
    list_display = ["book_name", "all_authors", "publisher", "language", "pub_date", "price", "category", "edit", "delete"]
    fieldsets = [
        [_("general information"), {"fields": ["book_name", "language", "pub_date"]}],
        [_("author & translator"), {"fields": ["author", "translator"]}],
        [_("description & excerpt"), {"fields": ["description", "excerpt"], "classes": ["collapse"]}],
        [_("more detail"), {"fields": ["publisher", "page", "height", "width"], "classes": ["collapse"]}],
        [_("image"), {"fields": ["image", "display_image"]}],
        [_("purchase information"), {"fields": ["price", "discount", "count"]}],
        [_("category & genre & tag"), {"fields": ["category", "genre", "tag"]}],
    ]
    readonly_fields = ["display_image"]

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:product_book_change', args=[obj.id]),
            translate
        )
    
    def all_authors(self, obj):
        return ", ".join(author.full_name for author in obj.author.all())
        

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:product_book_delete', args=[obj.id]),
            translate
        )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" style="background-color: #121212;"/>'.format(obj.image.url))
        else:
            return _("there is no image")

    all_authors.short_description = _("authors")
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
    display_image.short_description = _("preview")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("author").select_related("category", "discount")