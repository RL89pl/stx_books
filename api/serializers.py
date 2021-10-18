from rest_framework import serializers
from .models import Book, Author, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )

    def to_representation(self, value):
        return value.name


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('name', )

    def to_representation(self, value):
        return value.name


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'title',
            'authors',
            'published_date',
            'categories',
            'average_rating',
            'ratings_count',
            'thumbnail'
        ]

    def to_representation(self, instance):
        new_representation = super().to_representation(instance)
        new_representation["authors"] = AuthorSerializer(instance.authors.all(), many=True).data
        new_representation["categories"] = CategorySerializer(instance.categories.all(), many=True).data
        return new_representation

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        categories = validated_data.pop('categories')
        book = Book.objects.create(**validated_data)
        book.authors.set(authors)
        book.categories.set(categories)
        book.save()
        return book
