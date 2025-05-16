from rest_framework.routers import DefaultRouter
from .api_views import AdViewSet, ExchangeProposalViewSet

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'proposals', ExchangeProposalViewSet, basename='proposal')

urlpatterns = router.urls
