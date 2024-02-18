from django.contrib import admin
from .models import Discount
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    ordering = ["-id"]
    list_display_links = None
    list_display = ["code", "percent", "cash", "maximum", "count", "expire_date", "edit", "delete"]

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:discount_discount_change', args=[obj.id]),
            translate
        )
    
    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:discount_discount_delete', args=[obj.id]),
            translate
        )

    edit.short_description = _("view/edit")
    delete.short_description = _("delete")

    def get_queryset(self, request):
        return super().get_queryset(request)