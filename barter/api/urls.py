from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AdViewSet,
    ExchangeProposalViewSet,
    UserViewSet,
    CustomTokenRefreshView,
    CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'proposals', ExchangeProposalViewSet, basename='proposal')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls + [
    path(
        'token/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        CustomTokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
