import scrapy
import time
from getNews.items import GetnewsItem
class MLBSpider(scrapy.Spider):
    name = "MLBSpider"
    start_urls = ['https://news.ltn.com.tw/topic/MLB']

    def parse(self, response):
        for block in response.xpath('//ul[contains(@class, "searchlist")]//li'):
            href = block.xpath('.//a[contains(@class, "tit")]/@href').extract_first()
            # 爬取新聞正文內容
            yield response.follow(url=href, callback=self.parse_content)
        a_next = response.xpath('//a[contains(@class, "p_next")]/@href').extract_first()
        if a_next:
            # 爬下一頁
            yield response.follow(a_next, callback=self.parse)
        time.sleep(1)

    def parse_content(self, response):
        for body in response.xpath('//div[contains(@class, "news_content")]'):
            title = body.xpath('./h1/text()').get()
            date = body.xpath('.//div[contains(@class, "c_time")]/text()').get()
            contents = body.xpath('.//div[contains(@class, "news_p")]//p//text()').extract()
            content = ' '.join(contents)
            # 確認我們所需要的資料都不為空，如為空則不存入
            if body and title and date and content:
            	item = GetnewsItem()
            	item['title'] = title
            	item['date'] = date
            	item['content'] = content
            	yield item
