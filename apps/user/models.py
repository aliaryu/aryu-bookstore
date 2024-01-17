from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.urls import reverse


class User(AbstractUser):
    email = models.EmailField(
        verbose_name = _("email"),
        max_length = 255,
        unique = True,
    )
    phone = models.CharField(
        verbose_name = _("phone"),
        max_length = 11,
        unique = True,
    )
    birth_date = models.DateField(
        verbose_name = _("birth date"),
        blank = True,
        null = True,
    )
    is_active = models.BooleanField(
        verbose_name = _("active"),
        default = False,
        help_text = _(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    image = models.ImageField(
        verbose_name = _("image"),
        upload_to = "user_image/",
        blank = True,
        null = True,
    )
    is_delete = models.BooleanField(
        verbose_name = _("delete"),
        default=False,
    )

    def clean(self):
        super().clean()
        if self.image:
            width, height = self.image.width, self.image.height
            if width != height:
                raise ValidationError({"image": _("The image must be square. Width and height should be the same.")})

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def force_delete(self):
        super().delete()

    def undelete(self):
        self.is_delete = False
        self.save()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.username}"