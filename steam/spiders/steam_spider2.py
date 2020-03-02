import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class SteamSpider2(CrawlSpider):
    name = "steam_games2"
    allowed_domains = ("steampowered.com")
    start_urls = ["https://store.steampowered.com/search/?specials=1&page=0"]

    def parse(self, response):
        unwanted = ['\u2122', '\u00ae']
        rows = response.xpath('//div[@id="search_resultsRows"]')
        titles = rows.xpath('.//span[@class="title"]/text()').extract()
        prices = rows.xpath('.//div[@class="col search_price discounted responsive_secondrow"]/text()').extract()
        price_list = []
        rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="pagebtn"]/@href',)),
                      follow=True),)

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
        # next_page = response.xpath('//a[@class="pagebtn"]/@href').extract_first()
        # if next_page:
        #     request = scrapy.Request(url=next_page)
        #     yield request
