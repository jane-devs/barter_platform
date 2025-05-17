from rest_framework import permissions

from ads.services import filter_ads


class IsOwnerMixin:
    """
    Миксин для проверки, что текущий пользователь — владелец объекта.
    """

    def is_owner(self, obj):
        return obj.user == self.request.user


class IsOwnerPermission(permissions.BasePermission):
    """
    DRF пермишн для проверки, что объект принадлежит пользователю.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class AdsFilterMixin:
    """
    Миксин для фильтрации кверисета объявлений по параметрам:
    - Поиск (по заголовку и описанию),
    - Категория,
    - Состояние.
    Используется в Django CBV и в DRF ViewSet.
    """

    def get_search_param(self):
        return self.request.query_params.get(
            'search', ''
        ) if hasattr(self.request, 'query_params') else self.request.GET.get(
            'search', '')

    def get_category_param(self):
        return self.request.query_params.get(
            'category', '') if hasattr(
                self.request, 'query_params') else self.request.GET.get(
                    'category', '')

    def get_condition_param(self):
        return self.request.query_params.get(
            'condition', '') if hasattr(
                self.request, 'query_params') else self.request.GET.get(
                    'condition', '')

    def filter_ads_queryset(self, queryset):
        """
        Фильтрует кверисет объявлений по параметрам поиска,
        категории и состояния.
        """

        search = self.get_search_param()
        category = self.get_category_param()
        condition = self.get_condition_param()
        return filter_ads(queryset, search, category, condition)
