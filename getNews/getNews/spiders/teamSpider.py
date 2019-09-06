import scrapy
import time
from getNews.items import teamItem
class teamSpider(scrapy.Spider):
    name = "teamSpider"
    start_urls = ['https://zh.wikipedia.org/zh-tw/%E7%BE%8E%E5%9C%8B%E8%81%B7%E6%A5%AD%E6%A3%92%E7%90%83%E5%A4%A7%E8%81%AF%E7%9B%9F']
    def parse(self, response):
        for block in response.xpath('//table//tbody//tr//td//b//a'):
            href = block.xpath('./@href').get()
            # 爬取內容
            yield response.follow(url=href, callback=self.parse_content)
            time.sleep(1)

    def parse_content(self, response):
        titleblock = response.xpath('//div[contains(@class,"firstHeading")]')
        name = titleblock.xpath('./h1/text()').get()
        players = []
        for body in response.xpath('//td//ul//li'):
            player = body.xpath('.//span[contains(@data-orig-title)]/text()').get()
            players.append(player)
        # 確認我們所需要的資料都不為空，如為空則不存入
        item = teamItem()
        item['name'] = name
        item['players'] = players
        yield item
