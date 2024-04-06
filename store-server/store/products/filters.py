from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateTimeFilter, ChoiceFilter
from django import forms

from .models import Ad, Category, Reply


# поиск по объявлениям
class AdFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains', label='Поиск по объявлениям')
    category = ModelMultipleChoiceFilter(
        field_name='adcategory_category',
        queryset=Category.objects.all(),
        label='Категории',
        widget=forms.CheckboxSelectMultiple()
    )
    published_date = DateTimeFilter(
        field_name='published_date',
        lookup_expr='gte',
        label='Дата',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Ad
        fields = {
            'title',
            'category',
        }


# фильтрация откликов на объявления
class ReplyFilter(FilterSet):
    ad = ModelMultipleChoiceFilter(
        field_name='ad_id',
        queryset=Ad.objects.none(),
        label='Мои объявления',
        widget=forms.CheckboxSelectMultiple()
    )
    published_date = DateTimeFilter(
        field_name='published_date',
        lookup_expr='gte',
        label='Дата',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
    status = ChoiceFilter(choices=Reply.STATUS, label='Статус отклика')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.filters['ad'].queryset = Ad.objects.filter(author=user)
            self.queryset = self.queryset.filter(ad__author=user)

    class Meta:
        model = Reply
        fields = {
            'ad',
            'status',
        }