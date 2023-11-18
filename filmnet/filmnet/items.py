import scrapy
from scrapy_djangoitem import DjangoItem
from main.models import Movie, Category, Cast, Director, Author


class MovieItem(DjangoItem):
    django_model = Movie
    categories = scrapy.item.Field()
    casts = scrapy.item.Field()
    authors = scrapy.item.Field()
    directors = scrapy.item.Field()
    type = scrapy.item.Field()



class CategoryItem(DjangoItem):
    django_model = Category

class CastItem(DjangoItem):
    django_model = Cast

class DirectorItem(DjangoItem):
    django_model = Director

class AuthorItem(DjangoItem):
    django_model = Author
class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()