import django_filters
from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet
from django_filters import DateFilter
from .models import *
class OrderFilter(django_filters.FilterSet):
    FirstDate = DateFilter(field_name='date_created',lookup_expr='gte')
    EndDate = DateFilter(field_name='date_created',lookup_expr='lte')
    note = CharFilter(field_name='note',lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']