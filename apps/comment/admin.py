from django.contrib import admin
from .models import Comment
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    ordering = ["-id"]
    list_display_links = None
    list_display = ["user", "create_at", "for_model", "content_object", "short_text", "approve", "edit", "delete"]
    fieldsets = [
        [_("comment information"), {"fields": ["user", "for_model", "content_object", "create_at", "update_at"]}],
        [_("comment & answer"), {"fields": ["text", "answer", "approve", "is_delete"]}]
    ]
    readonly_fields = ["user", "create_at", "update_at", "for_model", "content_object"]
    
    def get_fieldsets(self, request, obj=None):
        if obj:
            return [
                [_("comment information"), {"fields": ["user", "for_model", "content_object", "create_at", "update_at"]}],
                [_("comment & answer"), {"fields": ["text", "answer", "approve", "is_delete"]}]
            ]
        else:
            return [
                [_("comment information"), {"fields": ["user", "content_type", "object_id"]}],
                [_("comment & answer"), {"fields": ["text", "answer", "approve", "is_delete"]}]
            ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        else:
            return ["create_at", "update_at", "for_model", "content_object"]

    def for_model(self, obj):
        return obj.content_object.__class__.__name__
    
    def short_text(self, obj):
        if len(obj.text) > 20:
            return obj.text[:20] + " ..."
        else:
            return obj.text

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:comment_comment_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:comment_comment_delete', args=[obj.id]),
            translate
        )

    for_model.short_description = _("model")
    short_text.short_description = _("short text")
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()