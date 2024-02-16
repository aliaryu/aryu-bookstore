from django.contrib import admin
from .models import (
    Category,
    Genre,
    Tag,
    Author,
    Book
)


admin.site.register([
    Category,
    Genre,
    Tag,
    Author,
    Book,
])