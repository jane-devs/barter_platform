import django_filters

from .models import Ad
from constants import ConstStr


class AdFilter(django_filters.FilterSet):
    """
    Фильтры для модели Ad:
    - По категории (без учёта регистра).
    - По состоянию (без учёта регистра).
    """

    category = django_filters.CharFilter(
        field_name=ConstStr.CATEGORY,
        lookup_expr='iexact'
    )
    condition = django_filters.CharFilter(
        field_name=ConstStr.CONDITION,
        lookup_expr='iexact'
    )

    class Meta:
        model = Ad
        fields = [ConstStr.CATEGORY, ConstStr.CONDITION]
