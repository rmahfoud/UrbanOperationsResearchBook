from scrapy.pipelines.files import FilesPipeline
import logging
import UrbanOperationsResearchBook as uor
import UrbanOperationsResearchBook.settings as settings
import os, shutil

logger = logging.getLogger(__name__)

class UORImagesPipeline(FilesPipeline):
    def item_completed(self, results, item, info):
        item = super(UORImagesPipeline, self).item_completed(results, item, info)
        logger.debug("Done with file download. Item: %s" % item['files'])
        for f in item['files']:
            from_path = os.path.join(settings.IMAGE_FILE_CACHE, f['path'])
            relative_path = uor.relative_url(settings.ROOT_URL, f['url'])
            to_path = os.path.join(settings.BOOK_FILES, relative_path)
            logger.debug("Copying %s to %s" % (from_path, to_path))
            if not os.path.isdir(os.path.dirname(to_path)):
                os.makedirs(os.path.dirname(to_path))
            shutil.copy(from_path, to_path)
        return item
