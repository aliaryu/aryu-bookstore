from django.urls import path
from .views import BookDetailView
from .api.views import (
    LikeUnlikeBookAPIView,
    SaveUnsaveBookAPIView,
    CommentBookAPIView
)


app_name = "product"

urlpatterns = [
    path("book/<int:pk>", BookDetailView.as_view(), name="book"),
    path("book/<int:pk>/likeunlike", LikeUnlikeBookAPIView.as_view(), name="likeunlike"),
    path("book/<int:pk>/saveunsave", SaveUnsaveBookAPIView.as_view(), name="saveunsave"),
    path("book/<int:pk>/comment", CommentBookAPIView.as_view(), name="bookcomment"),
]