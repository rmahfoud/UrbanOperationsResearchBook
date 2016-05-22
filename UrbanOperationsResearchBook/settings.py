# Scrapy settings for UrbanOperationsResearchBook project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

ALLOWED_DOMAIN = "web.mit.edu"
ROOT_URL = 'http://web.mit.edu/urban_or_book/www/book/'
SPIDER_NAME = 'uor'
ROOT_DIR = '/tmp/' + SPIDER_NAME
BOOK_DIR = ROOT_DIR + '/book'
CONTENT_DIR = BOOK_DIR + '/content'
ORIGINALS_DIR = ROOT_DIR + '/original-html'
IMAGE_FILE_CACHE = ROOT_DIR + '/image-cache/'

BOT_NAME = 'UrbanOperationsResearchBook'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['UrbanOperationsResearchBook.spiders']
NEWSPIDER_MODULE = 'UrbanOperationsResearchBook.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
ITEM_PIPELINES = {'UrbanOperationsResearchBook.pipelines.UORImagesPipeline': 1}
FILES_STORE = IMAGE_FILE_CACHE
