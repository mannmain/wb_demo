import django_filters
from .models import ColorVariant


class ColorVariantFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='card__brand', lookup_expr='iexact')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    color = django_filters.CharFilter(field_name='colors__name', lookup_expr='iexact')
    kind = django_filters.CharFilter(field_name='kinds__name', lookup_expr='iexact')

    class Meta:
        model = ColorVariant
        fields = ['card', 'brand', 'price_min', 'price_max', 'color', 'kind']
