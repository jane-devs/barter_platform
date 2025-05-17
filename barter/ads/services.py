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
