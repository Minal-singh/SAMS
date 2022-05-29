from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("administration/", admin.site.urls),
    path("", include("main_app.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "main_app.views.handle_not_found"
handler500 = "main_app.views.handle_server_error"
