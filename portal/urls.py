from django.urls import path, include
from django.views.generic import TemplateView

from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BookViewset)
router.register(r'authors', AuthorViewset)
router.register(r'category', CategoryViewset)


urlpatterns = [
    path('books/', BooksList.as_view(), name='books_list'),
    path('books/<int:pk>/', BookDetail.as_view()),
    path('authors/', AuthorList.as_view(), name='authors_list'),
    path('authors/<int:pk>/', AuthorDetail.as_view()),
    path('books/create/', BookCreate.as_view()),
    path('books/delete/<int:pk>/', BookDelete.as_view()),
    path('books/update/<int:pk>/', BookUpdate.as_view()),
    path('authors/update/<int:pk>/', AuthorUpdate.as_view()),
    path('books/my/', ListOfMyBooks.as_view()),
    path('books/search/', BooksWithFilter.as_view()),
    path('authors/search/', AuthorWithFilter.as_view()),
    path('books/like/<int:pk>/', like_book),
    path('books/dislike/<int:pk>', dislike_book),
    path('books/liked/', ListOfLikeBook.as_view(), name="list_of_like_books"),
    path('books/authors/liked/', TemplateView.as_view(template_name='books_and_authors_liked.html')),
    path('authors/like/<int:pk>', like_author),
    path('authors/dislike/<int:pk>', dislike_author),
    path('authors/liked/', ListOfLikeAuthor.as_view(), name="list_of_like_authors"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/documentation/', TemplateView.as_view(template_name= 'api_documentation.html'))
]
