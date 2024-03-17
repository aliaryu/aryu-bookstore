from django.urls import path
from .views import BookDetailView
from .api.views import LikeUnlikeBookAPIView


app_name = "product"

urlpatterns = [
    path("book/<int:pk>", BookDetailView.as_view(), name="book"),
    path("book/<int:pk>/likeunlike", LikeUnlikeBookAPIView.as_view(), name="likeunlike"),
]
