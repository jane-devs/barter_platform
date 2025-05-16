from django.contrib import admin
from django.urls import path, include
from ads.views import redirect_to_ads


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', redirect_to_ads),
    path('', include('ads.urls')),  # подключаем API
]
