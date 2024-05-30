import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors_by_srapy.json',
        'FEED_EXPORT_INDENT': 4 
    }

    def parse(self, response):
        author_links = response.css('small.author ~ a::attr(href)').getall()
        authors = response.css('small.author::text').getall()

        for author, link in zip(authors, author_links):
            yield response.follow(link, callback=self.parse_author, meta={'author': author})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            'fullname': response.css('h3.author-title::text').get().strip(),
            'born_date': response.css('span.author-born-date::text').get().strip(),
            'born_location': response.css('span.author-born-location::text').get().strip(),
            'description': response.css('div.author-description::text').get().strip(),
        }
