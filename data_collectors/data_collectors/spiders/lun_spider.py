import re

from scrapy import Selector
from scrapy.spiders import Spider, Request


class LunSpider(Spider):
    name = 'lun'
    start_urls = [
        'https://flatfy.lun.ua/uk/%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BA%D0%B8%D1%97%D0%B2?page=1']

    def parse(self, response):
        root = Selector(response=response)
        ads = root.xpath('//article')
        for ad in ads:
            ad_info = self.parse_article(ad)
            if ad_info:
                yield ad_info

        base_url, page_number = response.url.split('page=')
        if page_number != 100:
            next_page_url = f'{base_url}page={int(page_number) + 1}'
            yield Request(url=next_page_url, callback=self.parse)

    @staticmethod
    def parse_article(article_el):
        region = article_el.xpath('./div/div[2]/div/a[2]/text()').get()
        price = article_el.xpath('./div/div[2]/div[2]/div[1]/a/div/text()').get()
        number_of_rooms = article_el.xpath('./div/div[2]/div[2]/div[2]/ul[1]/li[1]/text()').get()
        area = article_el.xpath('./div/div[2]/div[2]/div[2]/ul[1]/li[2]/text()').get()

        if region and price and number_of_rooms and area:
            try:
                return {'region': region,
                        'price': LunSpider.parse_price(price),
                        'number_of_rooms': LunSpider.parse_numbers_of_room(number_of_rooms),
                        'area': LunSpider.parse_area(area),
                        'source': LunSpider.name}
            except ValueError:
                return None

    @staticmethod
    def parse_price(price):
        price = price.lower()
        price_in_dollars = '$' in price
        price = int(re.sub('[^0-9]', '', price))
        if not price_in_dollars:
            price = price // 28
        return price

    @staticmethod
    def parse_numbers_of_room(numbers_of_room):
        numbers_of_room = numbers_of_room.lower()
        if numbers_of_room.startswith('одно'):
            return 1
        return int(numbers_of_room[0])

    @staticmethod
    def parse_area(area):
        area = re.sub('[^0-9]', '', area.split('/')[0])
        return int(area)
