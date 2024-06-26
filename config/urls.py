from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),

    path("", include("apps.home.urls")),
    path("about/", include("apps.about.urls")),
    path("user/", include("apps.user.urls")),
    path("product/", include("apps.product.urls")),
    path("order/", include("apps.order.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
