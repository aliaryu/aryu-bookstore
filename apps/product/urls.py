from django.urls import path
from .views import BookDetailView


app_name = "product"

urlpatterns = [
    path("book/<int:pk>", BookDetailView.as_view(), name="book"),
]
