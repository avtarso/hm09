from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from quotes_scraper.quotes_scraper.spiders.quotes import QuotesSpider
from quotes_scraper.quotes_scraper.spiders.authors import AuthorsSpider


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())

    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()