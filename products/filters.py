import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    comment = django_filters.BooleanFilter(field_name='comment', method='filter_bool', label='Comment', )
    like = django_filters.BooleanFilter(field_name='like', method='filter_bool', label='Like')

    def filter_bool(self, queryset, name, value):
        lookup = '__'.join([name, 'isnull'])
        return queryset.filter(**{lookup: value})

    class Meta:
        model = Product
        fields = ['comment', 'like']
