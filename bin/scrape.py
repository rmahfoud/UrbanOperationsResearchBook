#! /usr/bin/python
import sys
sys.path.append('../UrbanOperationsResearchBook')

import UrbanOperationsResearchBook.settings as settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json, os, copy, shutil


def delete_keys_from_dict(d, keys):
    """
    Delete the keys if present in the dictionary.
    Loops recursively over nested dictionaries and other collections.
    """
    if isinstance(d, dict):
        for field in d.keys():
            if field in keys:
                del d[field]
            elif isinstance(d[field], dict) or isinstance(d[field], list) or isinstance(d[field], set):
                delete_keys_from_dict(d[field], keys)
    elif isinstance(d, dict) or isinstance(d, list) or isinstance(d, set):
        for i in d:
            delete_keys_from_dict(i, keys)
    
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    book = {'item_type': 'book', 'base_dir': settings.CONTENT_DIR}
    process.crawl('uor', book=book)
    process.start() # the script will block here until the crawling is finished

    # Easily-fixable misses in the original that we're correcting here
    book['additional_images'] = []
    missing = [['chapter2/pics/pi.gif', 'chapter2/images/pi.gif']]
    for missing_from, where_to_get in missing:
        print "Missing: %s, We can get from: %s" % (missing_from, where_to_get)
        shutil.copy(os.path.join(settings.CONTENT_DIR, where_to_get), os.path.join(settings.CONTENT_DIR, missing_from))
        book['additional_images'].append(missing_from)
        
    # Write full JSON of book metadata
    with open(os.path.join(settings.ROOT_DIR, "book.json"), "w") as fd:
        json.dump(book, fd, indent=1)

    # Write JSON without files and file_urls
    result_book_nofiles = copy.deepcopy(book)
    delete_keys_from_dict(result_book_nofiles, set(['file_urls', 'files']))
    with open(os.path.join(settings.ROOT_DIR, "book.nofiles.json"), "w") as fd:
        json.dump(result_book_nofiles, fd, indent=1)
