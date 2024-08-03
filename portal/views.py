from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView,TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string


class BooksList(ListView):
    model = Book
    template_name = "books_list.html"
    context_object_name = 'books'

class BookDetail(DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = 'book'

class AuthorList(ListView):
    model = Author
    template_name = "authors_list"
    context_object_name = "authors"

class AuthorDetail(DetailView):
    model = Author
    template_name = "author_detail"
    context_object_name = "author"

