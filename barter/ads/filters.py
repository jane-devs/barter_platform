import django_filters

from .models import Ad
from constants import ConstStr
from django.db.models import Q


def filter_ads(queryset, search=None, category=None, condition=None):
    """
    Применяет фильтрацию к набору объявлений по параметрам:
    - search: текстовое вхождение в заголовок или описание (поиск нечёткий).
    - category: точное совпадение категории.
    - condition: точное совпадение состояния.

    """
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    if category:
        queryset = queryset.filter(category__iexact=category)
    if condition:
        queryset = queryset.filter(condition__iexact=condition)
    return queryset


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
