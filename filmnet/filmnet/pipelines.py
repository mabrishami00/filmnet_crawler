# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from asgiref.sync import sync_to_async
from filmnet.filmnet.items import MovieItem, CategoryItem, CastItem
from main.models import Movie, Category, Cast, Director, Author
import re


def remove_tags(text):
    clean_text = re.sub("<[^<]+?>", "", text)
    return clean_text


class FilmnetPipeline:
    async def process_item(self, item, spider):
        await self.save_item_async(item)
        return item

    @sync_to_async
    def save_item_async(self, item):
        if isinstance(item, MovieItem):
            category_instances = []
            for category_item in item.get("categories", []):
                if not Category.objects.filter(title=category_item["title"]).exists():
                    category = Category(
                        type=category_item["type"], title=category_item["title"]
                    )
                    category_instances.append(category)
            Category.objects.bulk_create(category_instances)

            cast_instances = []
            for cast_item in item.get("casts", []):
                if not Cast.objects.filter(name=cast_item["name"]).exists():
                    cast = Cast(name=cast_item["name"])
                    cast_instances.append(cast)
            Cast.objects.bulk_create(cast_instances)

            director_instances = []
            for director_item in item.get("directors", []):
                if not Director.objects.filter(name=director_item["name"]).exists():
                    director = Director(name=director_item["name"])
                    director_instances.append(director)
            Director.objects.bulk_create(director_instances)

            author_instances = []
            for author_item in item.get("authors", []):
                if not Author.objects.filter(name=author_item["name"]).exists():
                    author = Author(name=author_item["name"])
                    author_instances.append(author)
            Author.objects.bulk_create(author_instances)

            if (
                not Movie.objects.filter(link=item["link"]).exists()
                and item["type"] == "single_video"
            ):
                item["summary"] = remove_tags(item["summary"])
                movie = Movie(
                    title=item.get("title"),
                    summary=item.get("summary"),
                    publish_date=item.get("publish_date"),
                    release_year=item.get("release_year"),
                    rate=item.get("rate"),
                    duration=item.get("duration"),
                    link=item.get("link"),
                )
                movie.save()
                movie.categories.add(*category_instances)
                movie.casts.add(*cast_instances)
                movie.authors.add(*author_instances)
                movie.directors.add(*director_instances)


                return movie
            return None

        # if isinstance(item, CategoryItem):
        #     if not Category.objects.filter(title=item["title"]).exists():
        #         category = Category(type=item["type"], title=item["title"])
        #         category.save()
        #         return category
        #     return None

        # if isinstance(item, ArtistItem):
        #     if not Artist.objects.filter(name=item["name"]).exists():
        #         artist = Artist(name=item["name"])
        #         artist.save()
        #         return artist
        #     return None
