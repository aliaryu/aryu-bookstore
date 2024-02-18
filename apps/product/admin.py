from django.contrib import admin
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    ordering = ["cat_name"]
    search_fields = ["cat_name"]
    list_display_links = None
    list_display = ["cat_name", "cat_parent", "edit", "delete"]
    fields = ["cat_name", "cat_parent", "display_image", "image"]
    readonly_fields = ["display_image"]

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
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" style="background-color: #121212;"/>'.format(obj.image.url))
        else:
            return _("there is no image")
    
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
    display_image.short_description = _("preview")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre
    ordering = ["genre_name"]
    search_fields = ["genre_name"]
    list_display_links = None
    list_display = ["genre_name", "short_description", "edit", "delete"]
    fields = ["genre_name", "description", "display_image", "image"]
    readonly_fields = ["display_image"]

    def short_description(self, obj):
        if len(obj.description) > 50:
            return obj.description[:50] + " ..."
        else:
            return obj.description

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
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" style="background-color: #121212;"/>'.format(obj.image.url))
        else:
            return _("there is no image")

    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
    short_description.short_description = _("description")
    display_image.short_description = _("preview")






admin.site.register([
    Tag,
    Author,
    Book,
])