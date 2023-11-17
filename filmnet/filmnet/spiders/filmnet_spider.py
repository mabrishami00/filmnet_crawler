import scrapy
import json

from main.models import Category
from filmnet.filmnet.items import MovieItem, CategoryItem, ImageItem


class FilmnetSpiderSpider(scrapy.Spider):
    name = "filmnet_spider"
    allowed_domains = ["filmnet.ir"]
    start_urls = [
        "https://filmnet.ir/api-v2/video-contents?offset=0&count=5&order=latest&query=&types=single_video&types=series&types=video_content_list"
    ]

    def parse(self, response):
        data = json.loads(response.body)
        movies = data.get("data")
        image_urls = []
        for movie in movies:
            category_names = []
            categories = movie.get("categories", [])
            for category in categories:
                items = category.get("items")
                for item in items:
                    category_item = CategoryItem()
                    category_item["type"] = category.get("type")
                    category_item["title"] = item.get("title")
                    category_names.append(item.get("title"))
                    yield category_item

            movie_item = MovieItem()
            movie_item["title"] = movie.get("title")
            movie_item["summary"] = movie.get("summary")
            movie_item["publish_date"] = movie.get("published_at")
            movie_item["release_year"] = movie.get("year")
            movie_item["rate"] = movie.get("rate")
            movie_item["duration"] = movie.get("duration")
            movie_item[
                "link"
            ] = f"https://filmnet.ir/contents/{movie.get('short_id')}/{movie.get('slug')}"
            movie_item["categories"] = category_names
            movie_item["type"] = movie.get("type")
            if movie.get("type") == "single_video":
                image_urls.append(movie.get("cover_image").get("path"))

            yield movie_item
        image_item = ImageItem()
        image_item["image_urls"] = image_urls
        yield image_item
