import scrapy
from scrapy_djangoitem import DjangoItem
from main.models import Movie, Category, Artist


class MovieItem(DjangoItem):
    django_model = Movie
    categories = scrapy.item.Field()
    artists = scrapy.item.Field()
    type = scrapy.item.Field()



class CategoryItem(DjangoItem):
    django_model = Category

class ArtistItem(DjangoItem):
    django_model = Artist

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()