from django.db import models


class Category(models.Model):
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Cast(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    publish_date = models.DateTimeField(null=True)
    release_year = models.IntegerField()
    rate = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    link = models.URLField(max_length=500)
    directors = models.ManyToManyField(Director)
    authors = models.ManyToManyField(Author)
    casts = models.ManyToManyField(Cast)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
