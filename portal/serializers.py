from .models import *
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name_category']


class AuthorSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'category']

    def create(self, validated_data):
        raise serializers.ValidationError("Вы не можете создать нового автора")


class BookSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'discription', 'author','category', 'user']

    def create(self, validated_data, **kwargs):
        categories = validated_data.pop("category")
        user = validated_data.pop("user")
        if not Author.objects.filter(user_id=user.id).exists():
            Author.objects.create(user_id=user.id, name=user.username)
        author_id = Author.objects.get(user_id=user.id).id
        book = Book.objects.create(**validated_data, author_id=author_id)

        for cat in categories:
            category = cat.pop("name_category")
            book.category.add(Category.objects.get(id=category))

        return book







