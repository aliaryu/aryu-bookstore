from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import min_percent_validator, max_percent_validator
from django.core.exceptions import ValidationError
import uuid


class Discount(models.Model):
    code = models.CharField(
        verbose_name = _("code"),
        max_length = 10,
        unique = True,
        blank = True,
        # editable = False,
    )
    percent = models.PositiveIntegerField(
        verbose_name = _("percent"),
        validators = [min_percent_validator, max_percent_validator],
        blank = True,
        null = True,
    )
    cash = models.PositiveIntegerField(
        verbose_name = _("cash"),
        blank = True,
        null = True,
    )
    maximum = models.PositiveIntegerField(
        verbose_name = _("maximum"),
    )
    count = models.PositiveIntegerField(
        verbose_name = _("count"),
        default = 1,
    )
    expire_date = models.DateTimeField(
        verbose_name = _("expire date"),
    )

    def clean(self):
        super().clean()
        if self.percent and self.cash:
            raise ValidationError(_("It is not possible to enter both 'percent' and 'cash'."))
        elif not self.percent and not self.cash:
            raise ValidationError(_("At least one of 'percent' and 'cash' must be entered."))
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4()).replace('-', '').upper()[:10]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("discount")
        verbose_name_plural = _("discounts")

    def __str__(self):
        if self.percent:
            return f"code: {self.code} - percent: {self.percent} %"
        else:
            return f"code: {self.code} - cash: {self.cash} $"

    def show_discount(self):
        if self.percent:
            return f"{self.percent}%"
        elif self.cash:
            return f"{self.cash:,}ت"