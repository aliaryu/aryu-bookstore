from django.urls import path
from .views import HomeView
from .api.views import ContactCreateAPIView


app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/",ContactCreateAPIView.as_view(), name="contact")
]
