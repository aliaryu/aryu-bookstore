from django.urls import path
from .views import (
    LoginView,
    SignUpView,
    ProfileView
)
from .api.views import (
    UserPassLoginView,
    UserSignUpView,
    UploadUserImageView,
    UserInfoUpdateView,
)
from django.contrib.auth.views import LogoutView


app_name = "user"

urlpatterns = [
    # LOGIN & LOGOUT & SIGNUP
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("userpass/", UserPassLoginView.as_view(), name="userpass"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("usersignup/", UserSignUpView.as_view(), name="usersignup"),

    # PROFILE
    path("profile/", ProfileView.as_view(), name="profile"),
    path("uploadimage/", UploadUserImageView.as_view(), name="uploadimage"),
    path("userinfo/", UserInfoUpdateView.as_view(), name="userinfo"),
]
