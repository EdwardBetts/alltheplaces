import scrapy

from locations.dict_parser import DictParser
from locations.spiders.vapestore_gb import clean_address


class FitnessFirstAUSpider(scrapy.Spider):
    name = "fitness_first_au"
    item_attributes = {"brand": "Fitness First", "brand_wikidata": "Q127120"}
    start_urls = ["https://api.fitnessfirst.com.au/clubs/v1/allclubs"]

    def parse(self, response, **kwargs):
        for gym in response.json()["clubs"]:
            gym.update(gym.pop("address"))
            item = DictParser.parse(gym)
            item["street_address"] = clean_address([gym.get("street1"), gym.get("street2")])
            item["website"] = f'https://www.fitnessfirst.com.au{gym["slug"]}'
            if gym["is24Hours"]:
                item["opening_hours"] = "24/7"

            yield item
