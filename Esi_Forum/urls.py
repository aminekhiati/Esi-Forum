from django.urls import include,path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
