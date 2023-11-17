from django.db import models


class Category(models.Model):
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Artist(models.Model):
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
    link = models.URLField(max_length=500, null=True)
    director = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return self.title
