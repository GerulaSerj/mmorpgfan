from django_filters import FilterSet, CharFilter, DateTimeFilter, ModelMultipleChoiceFilter
from django.forms import DateTimeInput
from .models import Advertisement, Category


class AdvertisementFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок:',
    )
    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата создания позднее:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )
    category = ModelMultipleChoiceFilter(
        field_name='advertisementCategory',
        queryset=Category.objects.all(),
        label='Category',
    )