import scrapy
from scrapy_djangoitem import DjangoItem
from main.models import Movie, Category


class MovieItem(DjangoItem):
    django_model = Movie
    categories = scrapy.item.Field()
    type = scrapy.item.Field()



class CategoryItem(DjangoItem):
    django_model = Category

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()