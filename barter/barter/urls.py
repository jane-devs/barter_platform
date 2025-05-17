from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

handler400 = 'ads.errors.handler400'
handler403 = 'ads.errors.handler403'
handler404 = 'ads.errors.handler404'
handler500 = 'ads.errors.handler500'


schema_view = get_schema_view(
   openapi.Info(
      title='API Платформы для бартера',
      default_version='v1',
      description=(
          'Тестовое задание для Effective Mobile 🚀.\n'
          'API для монолитного веб-приложение на Django \n'
          'для организации обмена вещами между пользователями.\n'
          '\n'
          'Автор: Скуратова Евгения\n'
          '📌 telegram: @janedoel\n'
          '📌 email: skuratovajj@gmail.com\n'
      ),
      contact=openapi.Contact(email='skuratovajj@gmail.com'),
      license=openapi.License(name='Тестовое задание'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   patterns=[
        path('api/', include('api.urls')),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', lambda request: redirect('ad_list', permanent=False)),
    path('', include('ads.urls')),
    path('api/', include('api.urls')),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
