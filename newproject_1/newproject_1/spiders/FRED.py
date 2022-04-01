import scrapy
import re



class FredSpider(scrapy.Spider):
    name = 'FRED'
    allowed_domains = ['fred.stlouisfed.org']
    start_urls = ['https://fred.stlouisfed.org/categories']

    def parse(self, response):
        links = response.css("span.fred-categories-child a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_blog_post_1)
        
    
    """unused code for reference as some href have diff structure followup links"""
    # def parse_blog_post(self, response):
    #     for div_selector in response.css('subcats.col-xs-12'):
    #         links4 = div_selector.css('div.col-xs-12.col-sm-6 a::attr(href)').getall()
    #         # linkextra = div_selector.css('div.col-xs-12.col-sm-10 a::attr(href)').getall()
        
    
    #         """for loop to go through the list4 and follow the links"""
    #         for link in links4:
    #             yield response.follow(link, callback=self.parse_blog_post_1)


    
    def parse_blog_post_1(self, response):
        for div_selector in response.css('div.col-xs-12.col-sm-6'):
            links2 = [re.sub(' ', '', ele) for ele in div_selector.css('ul.list-bullets a::attr(href)').getall()] 
            """used list comprehension to remove spaces 
            from href as they were not providing correct followup links"""
            for link in links2:
                yield response.follow(link, callback=self.parse_blog_post_2)
        
        """this directly calls back to the last function as there are no more followup links"""
        for div_selector in response.css('div.col-xs-12.col-sm-10'):
            links2 = response.css('div.col-xs-12.col-sm-10 a::attr(href)').getall()
            
            for link in links2:
                yield response.follow(link, callback=self.parse_blog_post_3)
        
    """this code can be directly used to get the series id for certian webpages"""
    # def parse_blog_post_x(self, response):
    #     linkextra = response.css('div.col-xs-12.col-sm-10 a::attr(href)').getall()
    #     for link in linkextra:
    #         yield response.follow(link, callback=self.parse_blog_post_3)
    
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