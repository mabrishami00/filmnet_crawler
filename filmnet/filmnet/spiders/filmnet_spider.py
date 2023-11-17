import scrapy
import json

from main.models import Category
from filmnet.filmnet.items import MovieItem, CategoryItem, ImageItem, ArtistItem


class FilmnetSpiderSpider(scrapy.Spider):
    name = "filmnet_spider"
    allowed_domains = ["filmnet.ir"]
    NUMBER_OF_MOVIES_EACH_REQUEST = 25
    OFFSET = 0
    start_urls = [
        f"https://filmnet.ir/api-v2/video-contents?offset={OFFSET}&count={NUMBER_OF_MOVIES_EACH_REQUEST}&order=latest&query=&types=single_video&types=series&types=video_content_list"
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
            link = f"https://filmnet.ir/contents/{movie.get('short_id')}/{movie.get('slug')}"
            movie_item["link"] = link
            movie_item["categories"] = category_names
            movie_item["type"] = movie.get("type")

            if movie.get("type") == "single_video":
                image_urls.append(movie.get("cover_image").get("path"))
                yield scrapy.Request(
                    link,
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
        all_tags = response.css(".css-165by6p").extract()
        artist_names = []
        for tag in all_tags:
            selector = scrapy.Selector(text=tag)

            if "بازیگر" in selector.css("p.css-1io4wcd.e1eum8tf0::text").get():
                artist_name = selector.css("p.css-1wuywbg.e1eum8tf0::text").get()
                artist_names.append(artist_name)
                artist_item = ArtistItem()
                artist_item["name"] = artist_name
                yield artist_item
            if "کارگردان" in selector.css("p.css-1io4wcd.e1eum8tf0::text").get():
                movie_item["director"] = selector.css(
                    "p.css-1wuywbg.e1eum8tf0::text"
                ).get()

            if "نویسنده" in selector.css("p.css-1io4wcd.e1eum8tf0::text").get():
                movie_item["author"] = selector.css(
                    "p.css-1wuywbg.e1eum8tf0::text"
                ).get()

        movie_item["artists"] = artist_names
        yield movie_item
