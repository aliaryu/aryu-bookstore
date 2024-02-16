from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import LogicalBaseModel, TimeStampBaseModel
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(LogicalBaseModel, TimeStampBaseModel):
    user = models.ForeignKey(
        verbose_name = _("user"),
        to = User,
        on_delete = models.CASCADE,
    )
    address = models.ForeignKey(
        verbose_name = _("address"),
        to = "user.Address",
        on_delete = models.SET_NULL,
        null = True,
        blank = False,
    )
    staff = models.ForeignKey(
        verbose_name = _("staff"),
        to = "user.Staff",
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )
    in_process = models.BooleanField(
        verbose_name = _("in process"),
        default = False,
    )
    is_complete = models.BooleanField(
        verbose_name = _("is complete"),
        default = False,
    )

    # Many-to-many Relation:

    book = models.ManyToManyField(
        verbose_name = _("book(s)"),
        to = "product.Book",
        through = "OrderBook",
    )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"order number: [ {self.id} ]"

