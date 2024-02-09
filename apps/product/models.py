from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import LogicalBaseModel
from .validators import min_percent_validator, max_percent_validator
from django.core.exceptions import ValidationError


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
    

class Tag(models.Model):
    tag_name = models.CharField(
        verbose_name = _("tag"),
        max_length = 255,
        unique = True,
    )

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return f"{self.tag_name}"
    

class Author(LogicalBaseModel):
    full_name = models.CharField(
        verbose_name = _("full name"),
        max_length = 255,
    )
    biography = models.TextField(
        verbose_name = _("biography"),
        blank = True,
    )
    nationality = models.CharField(
        verbose_name = _("nationality"),
        max_length = 255,
    )
    image = models.ImageField(
        verbose_name = _("image"),
        upload_to = "author_image/",
        blank = True,
        null = True,
    )


class Book(models.Model):
    pass


class Discount(models.Model):
    code = models.CharField(
        verbose_name = _("code"),
        max_length = 10,
        unique = True,
    )
    percent = models.PositiveIntegerField(
        verbose_name = _("percent"),
        validators = [min_percent_validator, max_percent_validator],
        blank = True,
        null = True,
    )
    cash = percent = models.PositiveIntegerField(
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

    class Meta:
        verbose_name = _("discount")
        verbose_name_plural = _("discounts")

    def __str__(self):
        if self.percent:
            return f"code: {self.code} - percent: {self.percent} %"
        else:
            return f"code: {self.code} - cash: {self.cash} $"
