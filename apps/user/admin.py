from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, Staff, Role
from django.utils.html import format_html
from django.urls import reverse


class AddressInline(admin.TabularInline):
    model = Address
    verbose_name = _("addresses")
    extra = 0
    classes = ["collapse"]


class StaffInline(admin.TabularInline):
    model = Staff
    verbose_name = _("staff information")
    classes = ["collapse"]
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    inlines = [AddressInline, StaffInline]
    ordering = ["username"]
    search_fields = ["username", "email", "last_name", "phone", "staff__role__role_name"]
    list_display_links = None
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "role", "edit", "delete"]
    fieldsets = [
        [_("unique information"), {"fields": ["username", "email", "phone"]}],
        [_("personal information"), {"fields": ["first_name", "last_name", "birth_date"]}],
        [_("image"), {"fields": ["image", "display_image"]}],
        [_("related dates"), {"fields": ["last_login", "date_joined"]}],
        [_("access level"), {"fields": ["is_superuser", "is_staff", "is_active", "is_delete"]}],
        [_("groups & permissions"), {"fields": ["groups", "user_permissions"], "classes": ["collapse"]}],
    ]
    readonly_fields = ["last_login", "date_joined", "display_image"]
    add_fieldsets = [
        [_("unique information"), {"fields": ["username", "email", "phone"]}],
        [_("personal information"), {"fields": ["first_name", "last_name", "birth_date"]}],
        [_("image"), {"fields": ["image", "display_image"]}],
        [_("access level"), {"fields": ["is_superuser", "is_staff", "is_active"]}],
        [_("password"), {"fields": ["password1", "password2"]}]
    ]

    def role(self, obj):
        if obj.is_superuser:
            return _("Superuser")
        elif obj.is_staff:
            return obj.staff.role.role_name
        else:
            return _("Customer")

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:user_user_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:user_user_delete', args=[obj.id]),
            translate
        )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" style="background-color: #121212;"/>'.format(obj.image.url))
        else:
            return _("there is no image")

    
    role.short_description = _("role")
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
    display_image.short_description = _("preview")
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.archive().select_related("staff__role")
        else:
            return super().get_queryset(request).select_related("staff__role")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address
    ordering = ["-id"]
    search_fields = ["postal_code", "user__username", "user__email"]
    list_display_links = None
    list_display = ["username", "postal_code", "province", "edit"]
    fields = ["user", "postal_code", "province", "address_path"]
    readonly_fields = ["user"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        else:
            return []

    def username(self, obj):
        return obj.user.username
    
    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:user_address_change', args=[obj.id]),
            translate
        )
    
    username.short_description = _("username")
    edit.short_description = _("view/edit")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    model = Role
    ordering = ["role_name"]
    search_fields = ["role_name"]
    list_display_links = None
    list_display = ["role_name", "salary", "edit"]
    fields = ["role_name", "salary", "is_delete"]

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:user_role_change', args=[obj.id]),
            translate
        )
    
    edit.short_description = _("view/edit")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    model = Staff
    ordering = ["-id"]
    search_fields = ["user__username", "user__email", "role__role_name"]
    list_display_links = None
    list_display = ["user", "role", "edit"]
    fields = ["user", "role"]

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:user_staff_change', args=[obj.id]),
            translate
        )
    
    edit.short_description = _("view/edit")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user").select_related("role")