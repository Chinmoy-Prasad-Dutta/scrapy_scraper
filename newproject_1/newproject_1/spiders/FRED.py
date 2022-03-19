import scrapy



class FredSpider(scrapy.Spider):
    name = 'FRED'
    allowed_domains = ['fred.stlouisfed.org']
    start_urls = ['https://fred.stlouisfed.org/categories']

    def parse(self, response):
        links = response.css("span.fred-categories-child a::attr(href)").getall()[0:3]
        for link in links:
            yield response.follow(link, callback=self.parse_blog_post)
        
    
    
    
    def parse_blog_post(self, response):
        for div_selector in response.css('div.col-xs-12.panel-menu'):
            links2 = div_selector.css('ul.list-bullets a::attr(href)').getall()
            for link in links2:
                yield response.follow(link, callback=self.parse_blog_post_2)
            # {
            #     'title': div_selector.css('ul.list-bullets a::attr(href)').getall(),
            #     'text': div_selector.css('ul.list-bullets a::text').getall()
            # }
    
    def parse_blog_post_2(self, response):
        for table_selector in response.css('table.table-responsive'):
            links3 = table_selector.css('tr.series-pager-title a::attr(href)').getall() #to get to the next page
            for link in links3:
                yield response.follow(link, callback=self.parse_blog_post_3)
                # yield{
                #     'title': table_selector.css('tr.series-pager-title a::attr(href)').getall(),
                #     'text': table_selector.css('tr.series-pager-title a::text').getall()
                # }
    
    
    def parse_blog_post_3(self, response):
        yield{
            'name' : response.css('h1.series-title span::text').getall()[1],
            'series_id' : response.css('h1.series-title a::attr(data-series-id)').getall(),
            
            
        }
        
    
    
    
    
    
    