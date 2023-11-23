import scrapy
import json

from main.models import Category
from filmnet.filmnet.items import (
    MovieItem,
    CategoryItem,
    ImageItem,
    CastItem,
    DirectorItem,
    AuthorItem,
)


class FilmnetSpiderSpider(scrapy.Spider):
    name = "filmnet_spider"
    allowed_domains = ["filmnet.ir"]
    NUMBER_OF_MOVIES_EACH_REQUEST = 2
    OFFSET = 0
    start_urls = [
        f"https://filmnet.ir/api-v2/video-contents?offset={OFFSET}&count={NUMBER_OF_MOVIES_EACH_REQUEST}&order=latest&query=&types=single_video&types=series&types=video_content_list"
    ]

    def parse(self, response):
        data = json.loads(response.body)
        movies = data.get("data")
        image_urls = []
        for movie in movies:
            category_items = []
            categories = movie.get("categories", [])
            for category in categories:
                items = category.get("items")
                for item in items:
                    category_item = CategoryItem()
                    category_item["type"] = category.get("type")
                    category_item["title"] = item.get("title")
                    category_items.append(category_item)

            movie_item = MovieItem()
            movie_item["title"] = movie.get("title")
            movie_item["summary"] = movie.get("summary")
            movie_item["publish_date"] = movie.get("published_at")
            movie_item["release_year"] = movie.get("year")
            movie_item["rate"] = movie.get("rate")
            movie_item["duration"] = movie.get("duration")
            link = f"https://filmnet.ir/contents/{movie.get('short_id')}/{movie.get('slug')}"
            movie_item["link"] = link
            movie_item["categories"] = category_items
            movie_item["type"] = movie.get("type")

            if movie.get("type") == "single_video":
                image_urls.append(movie.get("cover_image").get("path"))
                artist_link = f"https://filmnet.ir/_next/data/q21Yt6rkBGclcDbawKQ7u/contents/{movie.get('short_id')}/{movie.get('slug')}.json?id={movie.get('short_id')}&slug={movie.get('slug')}"
                yield scrapy.Request(
                    artist_link,
                    callback=self.parse_detail,
                    cb_kwargs={"movie_item": movie_item},
                )
        image_item = ImageItem()
        image_item["image_urls"] = image_urls
        yield image_item
        self.OFFSET += 25
        if self.OFFSET <= 100:
            next_link = f"https://filmnet.ir/api-v2/video-contents?offset={self.OFFSET}&count={self.NUMBER_OF_MOVIES_EACH_REQUEST}&order=latest&query=&types=single_video&types=series&types=video_content_list"
            yield response.follow(next_link, self.parse)

    def parse_detail(self, response, movie_item):
        json_data = json.loads(response.body)
        artists = (
            json_data.get("pageProps").get("aggregate").get("artists")
        )

        cast_items = []
        director_items = []
        author_items = []

        for artist in artists:
            if "بازیگر" in artist.get("roles"):
                cast_item = CastItem()
                cast_item["name"] = artist.get("person").get("name")
                cast_items.append(cast_item)
            if "کارگردان" in artist.get("roles"):
                director_item = DirectorItem()
                director_item["name"] = artist.get("person").get("name")
                director_items.append(director_item)
            if "نویسنده" in artist.get("roles"):
                author_item = AuthorItem()
                author_item["name"] = artist.get("person").get("name")
                author_items.append(author_item)

        movie_item["casts"] = cast_items
        movie_item["directors"] = director_items
        movie_item["authors"] = author_items

        yield movie_item
