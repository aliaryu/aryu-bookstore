from django.urls import path
from .views import LoginView, SignUpView
from .api.views import UserPassLoginView
from django.contrib.auth.views import LogoutView


app_name = "user"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("userpass/", UserPassLoginView.as_view(), name="userpass"),
    path("signup/", SignUpView.as_view(), name="signup")

]
