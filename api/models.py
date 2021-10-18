from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=155, unique=True, db_index=True)
    authors = models.ManyToManyField(Author)
    published_date = models.CharField(max_length=50, blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    ratings_count = models.PositiveIntegerField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
