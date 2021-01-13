import scrapy
from datetime import datetime
from ..items import HabrparserItem


class ResJournalSpider(scrapy.Spider):
    name = "resjournal"

    def start_requests(self):
        urls = [
            'https://research-journal.org/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        i = 0
        categories = response.css("li.cat-item")
        for category in categories:
            i += 1
            if i > 1:
                break
            category_link = category.css("a::attr(href)").extract_first()
            category_name = category.css("a::text").extract_first()

            item = HabrparserItem()
            item['category'] = category_name

            request = scrapy.Request(url=category_link, callback=self.parse_category)
            request.meta['item'] = item        
            # print("AAAAAAAAA: ",category.css("a::attr(href)").extract()[0])
            yield request
        
        # for category in response.css(".nav-links"):
            # yield{
            #     'link':annonce.css('::attr(href)').extract_first(),
            #     'title':annonce.css('.item_title::text').extract_first().strip(),
            #     }
            # print("CATEGORY::::::       ", category.css('li').extract())

    def parse_category(self, response):
        item = response.meta['item']
        articles = response.css("div.post.entry.clearfix.latest")
        next_page_exists = response.css("div.pagination.clearfix > div.alignleft > a::text").extract_first()
        while next_page_exists is not None:
            next_page_exists = response.css("div.pagination.clearfix > div.alignleft > a::text").extract_first()
            i=0
            for article in articles:
                i += 1
                if i>1:
                    break
                # print("ya tut           ", article.css("h3.title > a::attr(href)").extract())
                request = scrapy.Request(url=article.css("h3.title > a::attr(href)").extract_first(), callback=self.parse_each_article)
                request.meta['item'] = item

                yield request

        # print("YAAAAAAAAAAAAAAAAAAA    ", response.css("div.pagination.clearfix > div.alignleft >  a::text").extract_first())

    def parse_each_article(self, response):
        item = response.meta['item']
        article_block = response.css("div.entry.post.clearfix")
        # print("ya tut           ", article_block.css("h1.title::text").extract_first())
        article_title = article_block.css("h1.title::text").extract_first()
        article_text = article_block.css("p::text").extract()
        article_text = ' '.join(article_text)
        # print("ya tut         ", article_text)
        article_date = article_block.css("p.meta-info a::text")[2].extract()
        article_date = article_date.split(' ')
        del article_date[0]
        article_date = ' '.join(article_date)
        article_parsed_date = datetime.now()
        article_author = response.css("meta[name = 'citation_author']::attr(content)").extract_first()
        original_link = response.url

        print("AAAAAAAAABAAAAAAAAAAAAAAA      ", original_link)

        # подготовка данных для добавления в БД
        
       
        item['name'] = article_title
        
        item['content'] = article_text
        item['author'] = article_author
        item['date'] = article_date
        item['parsed_date'] = article_parsed_date
        item['source'] = 2
        item['original_link'] = original_link
        item['images'] = {}
        # добавление в БД
        yield item

        # array = ['ya', 'tut', 'privet', 'kakdela']
        # array = ' '.join(array)
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA     ", array)
