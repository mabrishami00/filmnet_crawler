import scrapy
import json

from main.models import Genre
from filmnet.filmnet.items import MovieItem, GenreItem


class FilmnetSpiderSpider(scrapy.Spider):
    name = "filmnet_spider"
    allowed_domains = ["filmnet.ir"]
    start_urls = [
        "https://filmnet.ir/api-v2/video-contents?offset=0&count=1&order=latest&query=&types=single_video&types=series&types=video_content_list"
    ]

    def parse(self, response):
        movie_item = MovieItem()
        data = json.loads(response.body)
        movies = data.get("data")
        for movie in movies:
            genres = movie.get("categories", [])
            genre_item = GenreItem()
            for genre in genres:
                genre_item["name"] = genre.get("type")
                # yield genre_item
            movie_item["title"] = movie.get("title")
            movie_item["summary"] = movie.get("summary")
            movie_item["publish_date"] = movie.get("published_at")
            movie_item["release_year"] = movie.get("year")
            movie_item["rate"] = movie.get("rate")
            movie_item["duration"] = movie.get("duration")
            movie_item["link"] = movie.get("link")

            genre_names = [genre.get('type') for genre in genres]
            # movie_item.instance.genres.add(*Genre.objects.filter(name__in=genre_names))

            yield movie_item




