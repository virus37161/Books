from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import Book_create_form, Author_update_form
from django.urls import reverse_lazy
from .filters import Book_filter_by_name, Books_filter, Author_filter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .serializers import *
import django_filters
from rest_framework.response import Response
from rest_framework import status, viewsets


class BooksList(ListView):
    model = Book
    template_name = "book/books_list.html"
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = Book_filter_by_name(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Author.objects.filter(user_id=self.request.user.id).exists():
            context['author_user'] = Author.objects.get(user_id=self.request.user.id)
        context['filterset'] = self.filterset
        return context


class BookDetail(DetailView):
    model = Book
    template_name = "book/book_detail.html"
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class AuthorList(ListView):
    model = Author
    template_name = "authors/authors_list.html"
    context_object_name = "authors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Author.objects.filter(user_id=self.request.user.id).exists():
            context['author_user'] = Author.objects.get(user_id=self.request.user.id)

        return context


class AuthorDetail(DetailView):
    model = Author
    template_name = "authors/author_detail.html"
    context_object_name = "author"


class BookCreate(LoginRequiredMixin, CreateView):
    form_class = Book_create_form
    model = Book
    template_name = "book/book_create.html"
    success_url = "/books/"

    def form_valid(self, form):
        book = form.save(commit=False)
        if not Author.objects.filter(user_id=self.request.user.id).exists():
            Author.objects.create(user_id=self.request.user.id, name=self.request.user.username)
        book.author_id = Author.objects.get(user_id=self.request.user.id).id
        self.object = form.save()
        return super().form_valid(form)


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('books_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.author_id == Author.objects.get(user_id=self.request.user.id).id:
            self.object.delete()
        else:
            return HttpResponseRedirect("Invalid Url")
        return HttpResponseRedirect(success_url)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/book_update.html'
    form_class = Book_create_form
    success_url = reverse_lazy('books_list')

    def form_valid(self, form):
        if self.object.author_id == Author.objects.get(user_id=self.request.user.id).id:
            self.object = form.save()
        else:
            return HttpResponseRedirect("Invalid Url")
        return super().form_valid(form)


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    template_name = 'authors/author_update.html'
    form_class = Author_update_form
    success_url = reverse_lazy('books_list')

    def form_valid(self, form):
        if self.object.user_id == self.request.user.id:
            self.object = form.save()
        else:
            return HttpResponseRedirect("Invalid Url")
        return super().form_valid(form)


class ListOfMyBooks(ListView):
    model = Book
    template_name = 'book/list_of_my_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.filter(author_id=self.request.user.author.id).all()
        return queryset


class BooksWithFilter(ListView):
    model = Book
    template_name = 'book/books_with_filter.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = Books_filter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AuthorWithFilter(ListView):
    model = Author
    template_name = 'authors/author_with_filter.html'
    context_object_name = 'authors'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = Author_filter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@login_required
def like_book(request, pk):
    user = request.user
    book = Book.objects.get(id=pk)
    book.favourite.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/books/{pk}/'))


@login_required
def dislike_book(request, pk):
    user = request.user
    book = Book.objects.get(id=pk)
    book.favourite.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/books/liked/'))


class ListOfLikeBook(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/list_of_like_book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = Book.objects.filter(favourite=self.request.user.id)
        return context


@login_required
def like_author(request, pk):
    user = request.user
    author = Author.objects.get(id=pk)
    author.favourite.add(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/authors/{pk}/'))


@login_required
def dislike_author(request, pk):
    user = request.user
    author = Author.objects.get(id=pk)
    author.favourite.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/authors/liked/'))


class ListOfLikeAuthor(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'authors/list_of_like_authors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = Author.objects.filter(favourite=self.request.user.id)
        return context


class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["id", "category"]

    def destroy(self, request, pk):
        instance = self.get_object()
        if instance.author_id == Author.objects.get(user_id=request.user.id).id:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValueError ("Вы не имеете на это право")


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["id", 'name']

    def destroy (self,request,pk):
        instance = self.get_object()
        if request.user.id == 1:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValueError("Вы не имеет права на удаление автора")


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["id", 'name_category']