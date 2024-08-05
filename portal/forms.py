from django import forms
from .models import Book, Author

class Book_create_form(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['name', 'discription','category']


class Author_update_form(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'category']