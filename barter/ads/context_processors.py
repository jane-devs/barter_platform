from django.db.models import Q

from .models import ExchangeProposal
from constants import ConstStr


def pending_proposals_count(request):
    """
    Добавляет в контекст шаблона количество необработанных заявок на обмен
    для текущего пользователя.

    Возвращает словарь с ключом 'pending_proposals_count' и числом заявок
    со статусом 'pending', в которых пользователь участвует
    как отправитель или получатель.
    """

    if request.user.is_authenticated:
        user_ads = request.user.ads.all()
        count = ExchangeProposal.objects.filter(
            Q(ad_receiver__in=user_ads) | Q(ad_sender__in=user_ads),
            status=ConstStr.PENDING
        ).count()
        return {'pending_proposals_count': count}
    return {}
