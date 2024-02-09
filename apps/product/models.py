from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    cat_name = models.CharField(
        verbose_name = _("category"),
        max_length = 255,
        unique = True,
    )
    cat_parent = models.ForeignKey(
        verbose_name = _("parent"),
        to = "self",
        on_delete = models.CASCADE
    )
    image = models.ImageField(
        verbose_name = _("image"),
        upload_to = "category_image/",
        blank = True,
        null = True,
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f"{self.cat_name}"


class Genre(models.Model):
    genre_name = models.CharField(
        verbose_name = _("genre"),
        max_length = 255,
        unique = True,
    )
    description = models.TextField(
        verbose_name = _("description"),
        blank = True,
    )
    image = models.ImageField(
        verbose_name = _("image"),
        upload_to = "genre_image/",
        blank = True,
        null = True,
    )

    class Meta:
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self):
        return f"{self.genre_name}"