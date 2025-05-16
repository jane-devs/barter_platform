from .models import ExchangeProposal
from django.db.models import Q


def pending_proposals_count(request):
    if request.user.is_authenticated:
        user_ads = request.user.ads.all()
        count = ExchangeProposal.objects.filter(
            Q(ad_receiver__in=user_ads) | Q(ad_sender__in=user_ads),
            status='pending'
        ).count()
        return {'pending_proposals_count': count}
    return {}