from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter,CharFilter,ModelChoiceFilter
from .models import Book, Author,Category
from django import forms

class Book_filter_by_name(FilterSet):
    class Meta:
        model = Book
        fields = ['name']

class Books_filter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='category', queryset=Category.objects.all(), label='Жанры',
                                         conjoined=True
    )
    class Meta:
        model = Book
        fields = ['name', 'author', 'category', 'rating']

class Author_filter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='category', queryset=Category.objects.all(), label='Жанры',
        conjoined=True
    )
    class Meta:
        model = Author
        fields = ['name', 'category']