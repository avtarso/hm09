import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes_by_srapy.json',
        'FEED_EXPORT_INDENT': 4 
    }

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'tags': quote.css('meta.keywords::attr(content)').get().split(','),
                'author': quote.css('small.author::text').get(),
                'quote': quote.css('span.text::text').get()
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
