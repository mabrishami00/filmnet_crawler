# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from asgiref.sync import sync_to_async
from filmnet.filmnet.items import MovieItem
from main.models import Movie
import re

def remove_tags(text):
    clean_text = re.sub('<[^<]+?>', '', text)
    return clean_text

class FilmnetPipeline:
    async def process_item(self, item, spider):
        await self.save_item_async(item)
        return item

    @sync_to_async
    def save_item_async(self, item):
        item["summary"] = remove_tags(item["summary"])
        movie = Movie(
            title=item["title"],
            summary=item["summary"],
            publish_date=item["publish_date"],
            release_year=item["release_year"],
            rate=item["rate"],
            duration=item["duration"],
            link=item["link"],
        )
        print(movie)
        print("$"*100)
        movie.save()
        return movie
