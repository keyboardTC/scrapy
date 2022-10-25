import scrapy
from scrapbullet.items import ScrapbulletItem
from scrapbullet.itemsloaders import ChocolateProductLoader


class NikespiderSpider(scrapy.Spider):

    #the name of the spider
    name = 'nikespider'
    #these are the urls that we will start scraping
    allowed_domains = ['chocolate.co.uk']

    #the url of the first page that we will start scraping
    start_urls = ['https://www.chocolate.co.uk/collections/all']

    def parse(self, response):

        product_item = ScrapbulletItem();
        
        #here we are looping through the products and extracting the name, price & url
        products = response.css('product-item')

        for product in products:
            #here we put the data returned into the format we want to output for our csv or json 
            
            # product_item['name'] = product.css('a.product-item-meta__title::text').get()
            # product_item['price'] = product.css('span.price').get().replace('<span class="price">\n <span class="visually-hidden">Sale price</span>','').replace('</span>','')
            # product_item['url'] = product.css('div.product-item-meta a').attrib['href']
            # yield product_item

            chocolate = ChocolateProductLoader(item=ScrapbulletItem(), selector=product)
            chocolate.add_css('name', "a.product-item-meta__title::text")
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
           next_page_url = 'https://www.chocolate.co.uk' + next_page
           yield response.follow(next_page_url, callback=self.parse)
