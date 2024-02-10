from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import LogicalBaseModel


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


class Book(LogicalBaseModel):

    # Fields:

    book_name = models.CharField(
        verbose_name = _("book name"),
        max_length = 255,
    )
    publisher = models.CharField(
        verbose_name = _("publisher"),
        max_length = 255,
    )
    description = models.TextField(
        verbose_name = _("description"),
        blank = True,
    )
    excerpt = models.TextField(
        verbose_name = _("excerpt"),
        blank = True,
    )
    pub_date = models.DateField(
        verbose_name = _("pub date"),
    )
    language = models.CharField(
        verbose_name = _("language"),
        max_length = 255,
    )
    height = models.PositiveIntegerField(
        verbose_name = _("height"),
    )
    width = models.PositiveIntegerField(
        verbose_name = _("width"),
    )
    page = models.PositiveIntegerField(
        verbose_name = _("page"),
    )
    count = models.PositiveIntegerField(
        verbose_name = _("count"),
    )
    price = models.DecimalField(
        verbose_name = _("price"),
        max_digits = 10,
        decimal_places = 2
    )
    image = models.ImageField(
        verbose_name = _("image"),
        upload_to = "book_image/",
    )

    # Relations:

    discount = models.ForeignKey(
        verbose_name = _("discount"),
        to = "discount.Discount",
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )
    category = models.ForeignKey(
        verbose_name = _("category"),
        to = "product.Category",
        on_delete = models.SET_NULL,
        null = True,
    )
    author = models.ManyToManyField(
        verbose_name = _("author(s)"),
        to = "product.Author",
        related_name = "author_books",
    )
    translator = models.ManyToManyField(
        verbose_name = _("translator(s)"),
        to = "product.Author",
        related_name = "translator_books",
    )
    genre = models.ManyToManyField(
        verbose_name = _("genre(s)"),
        to = "product.Genre",
    )
    tag = models.ManyToManyField(
        verbose_name = _("tag(s)"),
        to = "product.Tag",
    )
    like = models.ManyToManyField(
        verbose_name = _("like(s)"),
        to = "user.User",
    )

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")

    def __str__(self):
        return f"{self.book_name}"