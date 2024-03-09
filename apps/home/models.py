from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampBaseModel


class Contact(TimeStampBaseModel):
    full_name = models.CharField(
        verbose_name = _("full name"),
        max_length = 255,
    )
    email = models.EmailField(
        verbose_name = _("email"),
        max_length = 255,
    )
    text = models.TextField(
        verbose_name = _("text"),
    )
    read = models.BooleanField(
        verbose_name = _("read"),
        default = False,
    )

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return f"{self.email} - {self.text[:10]}"
