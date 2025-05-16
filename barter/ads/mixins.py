from .services import filter_ads
from rest_framework import permissions


class IsOwnerMixin:
    def is_owner(self, obj):
        return obj.user == self.request.user


class IsOwnerPermission(permissions.BasePermission):
    """
    DRF permission для проверки, что объект принадлежит пользователю
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class AdsFilterMixin:
    def get_search_param(self):
        # Для DRF будет request.query_params, для Django CBV — request.GET
        if hasattr(self.request, 'query_params'):
            return self.request.query_params.get('search', '')
        return self.request.GET.get('search', '')

    def get_category_param(self):
        if hasattr(self.request, 'query_params'):
            return self.request.query_params.get('category', '')
        return self.request.GET.get('category', '')

    def get_condition_param(self):
        if hasattr(self.request, 'query_params'):
            return self.request.query_params.get('condition', '')
        return self.request.GET.get('condition', '')

    def filter_ads_queryset(self, queryset):
        search = self.get_search_param()
        category = self.get_category_param()
        condition = self.get_condition_param()
        return filter_ads(queryset, search, category, condition)
