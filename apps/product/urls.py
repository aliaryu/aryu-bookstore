from django.urls import path
from .views import (
    BookDetailView,
    AuthorDetailView,
    CategoryListView,
    GenreListView,
    TagListView,
    AllBooksListView,
    DiscountBooksListView,
    SearchListView
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
    path("genre/<int:pk>/", GenreListView.as_view(), name="genre"),
    path("tag/<int:pk>/", TagListView.as_view(), name="tag"),
    path("allbooks/", AllBooksListView.as_view(), name="allbooks"),
    path("discountbooks/", DiscountBooksListView.as_view(), name="discountbooks"),

    # SEARCH
    path("search/", SearchListView.as_view(), name="search"),
]
