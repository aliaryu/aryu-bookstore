from django.urls import path
from .views import LoginView
from .api.views import UserPassLoginView


app_name = "user"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("userpass/", UserPassLoginView.as_view(), name="userpass"),
]
