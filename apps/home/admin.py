from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact
    ordering = ["-id"]
    search_fields = ["email", "full_name"]
    list_display_links = None
    list_display = ["full_name", "email", "read", "edit", "delete"]
    fieldsets = [
        [_("sender information"), {"fields": ["full_name", "email"]}],
        [_("date & time"), {"fields": ["create_at", "update_at"]}],
        [_("message & status"), {"fields": ["read", "text"]}],
    ]
    readonly_fields = ["create_at", "update_at"]

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:home_contact_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:home_contact_delete', args=[obj.id]),
            translate
        )

    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
