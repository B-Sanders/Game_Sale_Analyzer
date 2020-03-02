import time

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class SteamSpider(scrapy.Spider):
    name = "steam_games"
    start_urls = ["https://store.steampowered.com/search/?specials=1&page=0"]
    # rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="pagebtn"]/@href',)),
    #               follow=True),)

    def parse(self, response):
        unwanted = ['\u2122', '\u00ae']
        rows = response.xpath('//div[@id="search_resultsRows"]')
        titles = rows.xpath('.//span[@class="title"]/text()').extract()
        prices = rows.xpath('.//div[@class="col search_price discounted responsive_secondrow"]/text()').extract()
        price_list = []

        for price in prices:
            if price[0] == '$':
                price_list.append(price)
        for i in range(len(price_list)):
            price_list[i] = price_list[i].replace(" ", "")

        for j in range(len(price_list)):
            titles[j] = ''.join([k for k in titles[j] if k not in unwanted])
            yield {
                "title": titles[j],
                "price": price_list[j]
            }
        next_page_list = response.xpath('//a[@class="pagebtn"]/@href').extract()
        if len(next_page_list) > 1:
            next_page = next_page_list[1]
        elif len(next_page_list) == 1:
            next_page = next_page_list[0]
        else:
            next_page = None

        if next_page:
            request = scrapy.Request(url=next_page)
            yield request
