from django.urls import path
from .views import (
    BookDetailView,
    AuthorDetailView,
    CategoryListView
)
from .api.views import (
    LikeUnlikeBookAPIView,
    SaveUnsaveBookAPIView,
    CommentBookAPIView,
    CommentAuthorAPIView
)


app_name = "product"

urlpatterns = [
    # BOOK
    path("book/<int:pk>/", BookDetailView.as_view(), name="book"),
    path("book/<int:pk>/likeunlike", LikeUnlikeBookAPIView.as_view(), name="likeunlike"),
    path("book/<int:pk>/saveunsave", SaveUnsaveBookAPIView.as_view(), name="saveunsave"),
    path("book/<int:pk>/comment", CommentBookAPIView.as_view(), name="bookcomment"),

    # AUTHOR
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author"),
    path("author/<int:pk>/comment", CommentAuthorAPIView.as_view(), name="authorcomment"),

    # LISTS
    path("category/<int:pk>/", CategoryListView.as_view(), name="category"),
]
