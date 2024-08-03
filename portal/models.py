from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name_category = models.TextField(unique= True)

    def __str__(self):
        return f'{self.name_category.title()}'

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 15, verbose_name= "Имя")
    category = models.ManyToManyField(Category, blank = True, verbose_name="Жанры", through="AuthorCategory")
    save = models.ManyToManyField(User, related_name = "save_authors", blank = True)

    def __str__(self):
        return f'{self.name.title()}'

class Book(models.Model):
     author = models.ForeignKey(Author, blank = False, on_delete = models.CASCADE, verbose_name="Автор")
     name = models.CharField(max_length=15, blank = False, verbose_name="Название")
     discription = models.TextField(verbose_name="Описание", blank = True, default="У данной книги нет описания")
     rating = models.IntegerField(default = 0, blank = True)
     category = models.ManyToManyField(Category, through="BookCategory", blank = True)
     save = models.ManyToManyField(User, related_name="save_book")

class BookCategory (models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class AuthorCategory(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)