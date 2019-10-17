from minet.crawl import crawl
from minet.utils import load_definition

spider = load_definition('./ftest/spiders/echojs_scraper.yml')

for result in crawl(spider):
    for item in result.scraped:
        print(item['title'])
