from django.urls import path, include
from .views import *

urlpatterns = [
    path('books/', BooksList.as_view(), name = 'books_list'),
    path('books/<int:pk>/', BookDetail.as_view()),
    path('authors/', AuthorList.as_view(), name = 'authors_list'),
    path('authors/<int:pk>/', AuthorDetail.as_view()),

]