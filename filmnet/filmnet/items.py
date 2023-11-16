import scrapy
from scrapy_djangoitem import DjangoItem
from main.models import Movie, Genre


class MovieItem(DjangoItem):
    django_model = Movie


class GenreItem(DjangoItem):
    django_model = Genre
