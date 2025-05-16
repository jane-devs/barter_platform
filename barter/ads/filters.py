import django_filters
from .models import Ad

class AdFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    condition = django_filters.CharFilter(field_name='condition', lookup_expr='iexact')

    class Meta:
        model = Ad
        fields = ['category', 'condition']