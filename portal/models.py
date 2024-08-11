from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name_category = models.TextField(unique= True)

    def __str__(self):
        return f'{self.name_category.title()}'

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=15, verbose_name="Имя")
    category = models.ManyToManyField(Category, verbose_name="Жанры", related_name="author_category")
    favourite = models.ManyToManyField(User, related_name="save_authors", blank=True)

    def __str__(self):
        return f'{self.name.title()}'

class Book(models.Model):
     author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
     name = models.TextField(blank=False, verbose_name="Название")
     discription = models.TextField(verbose_name="Описание", blank=True, default="У данной книги нет описания")
     rating = models.IntegerField(default=0, blank=True)
     category = models.ManyToManyField(Category, related_name="book_category", blank=True)
     favourite = models.ManyToManyField(User, related_name="save_book", blank=True)

     def __str__(self):
         return f'{self.name.title()}'

