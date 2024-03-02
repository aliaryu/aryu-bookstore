from django.contrib import admin
from .models import Order, OrderBook, OrderStaff
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse


class OrderBookInline(admin.TabularInline):
    model = OrderBook
    extra = 0
    fields = ["book", "count", "get_item_price"]
    readonly_fields = ["get_item_price"]

    def get_item_price(self, obj):
        return obj.book.price
    
    get_item_price.description = _("price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderBookInline]
    ordering = ["-id"]
    search_fields = ["id", "user__username", "user__email"]
    list_display_links = None
    list_display = ["__str__", "user", "staff", "create_at", "status", "edit", "delete"]
    fieldsets = [
        [_("customer information"), {"fields": ["user", "get_user_fullname", "get_user_phone", "address", "full_address"]}],
        [_("order information"), {"fields": ["staff", "create_at", "update_at", "status", "get_total_cost"]}]
    ]
    readonly_fields = ["user", "staff", "get_user_fullname", "get_user_phone", "full_address", "create_at", "update_at", "get_total_cost"]

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ["get_user_fullname", "get_user_phone", "full_address", "create_at", "update_at", "get_total_cost"]
        else:
            if request.user.is_superuser:
                return ["get_user_fullname", "get_user_phone", "full_address", "create_at", "update_at", "get_total_cost"]
        return super().get_readonly_fields(request, obj)

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:order_order_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:order_order_delete', args=[obj.id]),
            translate
        )
    
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()
    
    def get_user_phone(self, obj):
        return obj.user.phone
    
    def full_address(self, obj):
        return f"city: {obj.address.get_province_display()}\npostal code: {obj.address.postal_code}\naddress: {obj.address.address_path}"
    
    def get_total_cost(self, obj):
        return sum(order_book.book.price * order_book.count for order_book in obj.orderbook_set.all())
    
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
    get_user_fullname.short_description = _("full name")
    get_user_phone.short_description = _("phone")
    full_address.short_description = _("full address")
    get_total_cost.short_description = _("total cost")

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request).select_related("user", "staff__user", "address")
        elif request.user.is_staff:
            return super().get_queryset(request).filter(status="PEN").select_related("user", "staff__user", "address")
        
    def save_model(self, request, obj, form, change):
        if obj.status == "PEN":
            if request.user.is_staff:
                obj.staff = None
        elif obj.status == "PRO":
            if request.user.is_staff:
                obj.staff = request.user.staff
        elif obj.status == "COM":
            if request.user.is_staff:
                obj.staff = request.user.staff
        elif obj.status == "DEL":
            if request.user.is_staff:
                obj.staff = request.user.staff
        obj.save()


@admin.register(OrderStaff)
class OrderStaffAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderBookInline]
    ordering = ["-id"]
    search_fields = ["id", "user__username", "user__email"]
    list_display_links = None
    list_display = ["__str__", "user", "staff", "create_at", "status", "edit", "delete"]
    fieldsets = [
        [_("customer information"), {"fields": ["user", "get_user_fullname", "get_user_phone", "address", "full_address"]}],
        [_("order information"), {"fields": ["staff", "create_at", "update_at", "status", "get_total_cost"]}]
    ]
    readonly_fields = ["user", "staff", "get_user_fullname", "get_user_phone", "full_address", "create_at", "update_at", "get_total_cost"]

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ["get_user_fullname", "get_user_phone", "full_address", "create_at", "update_at", "get_total_cost"]
        else:
            if request.user.is_superuser:
                return ["get_user_fullname", "get_user_phone", "full_address", "create_at", "update_at", "get_total_cost"]
        return super().get_readonly_fields(request, obj)

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:order_orderstaff_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:order_orderstaff_delete', args=[obj.id]),
            translate
        )
    
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()
    
    def get_user_phone(self, obj):
        return obj.user.phone
    
    def full_address(self, obj):
        return f"city: {obj.address.get_province_display()}\npostal code: {obj.address.postal_code}\naddress: {obj.address.address_path}"
    
    def get_total_cost(self, obj):
        return sum(order_book.book.price * order_book.count for order_book in obj.orderbook_set.all())
    
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")
    get_user_fullname.short_description = _("full name")
    get_user_phone.short_description = _("phone")
    full_address.short_description = _("full address")
    get_total_cost.short_description = _("total cost")

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request).select_related("user", "staff__user", "address")
        elif request.user.is_staff:
            return super().get_queryset(request).filter(staff=request.user.staff).select_related("user", "staff__user", "address")
        
    def save_model(self, request, obj, form, change):
        if obj.status == "PEN":
            if request.user.is_staff:
                obj.staff = None
        elif obj.status == "PRO":
            if request.user.is_staff:
                obj.staff = request.user.staff
        elif obj.status == "COM":
            if request.user.is_staff:
                obj.staff = request.user.staff
        elif obj.status == "DEL":
            if request.user.is_staff:
                obj.staff = request.user.staff
        obj.save()


@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    model = OrderBook
    ordering = ["-id"]
    list_display_links = None
    list_display = ["book", "order", "get_order_datetime", "count", "edit", "delete"]
    fields = ["book", "order", "count", "is_delete"]

    def get_order_datetime(self, obj):
        return obj.order.create_at

    def edit(self, obj):
        translate = _("view/edit")
        return format_html(
            '<a class="button" href="{}">{}</a>',
            reverse('admin:order_orderbook_change', args=[obj.id]),
            translate
        )

    def delete(self, obj):
        translate = _("delete")
        return format_html(
            '<a class="button" href="{}" style="color:white; background-color: #840303 ;">{}</a>',
            reverse('admin:order_orderbook_delete', args=[obj.id]),
            translate
        )
    
    get_order_datetime.short_description = _("date time")
    edit.short_description = _("view/edit")
    delete.short_description = _("delete")