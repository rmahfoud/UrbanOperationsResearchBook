#! /usr/bin/python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('uor')
    process.start() # the script will block here until the crawling is finished