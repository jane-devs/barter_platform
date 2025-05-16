from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdViewSet, ExchangeProposalViewSet

from . import views


router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'proposals', ExchangeProposalViewSet, basename='proposal')

urlpatterns = [
    path('api/', include(router.urls)),
    path('ads/create/', views.create_ad, name='ad_create'),
    path('ads/<int:pk>/update/', views.update_ad, name='ad_update'),
    path('ads/<int:pk>/delete/', views.delete_ad, name='ad_delete'),
    path('ads/', views.ad_list, name='ad_list'),
    path('proposals/create/', views.create_proposal, name='proposal_create'),
]
