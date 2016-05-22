'''
@author: rmahfoud
'''

import UrbanOperationsResearchBook.settings as settings
import UrbanOperationsResearchBook as uor
import os, re, shutil
import logging

logger = logging.getLogger(__name__)

class UORProblemsGenerator():
    MISSING_CONTENT_FILE = "#"
    current_indent = 0

    def __init__(self, book, *args, **kwargs):
        self.book = book
    
    def relative_url(self, path):
        return uor.relative_url(self.book['base_dir'], path)

    def generateProblemsContent(self):
        for chapter_no in self.book['chapters'].keys():
            self.generateChapterProblemsContent(self.book['chapters'][chapter_no])
    
    def generateChapterProblemsContent(self, chapter):
        section = [section for section in chapter['sections'] \
                           if section['section_type'] == 'problems' and not 'content_file' in section]
        if len(section) == 0:
            return
        if len(section) > 1:
            raise "More than one problem sections in chapter %s" % chapter['no']
        section = section[0]
        problems = section['problems']
        if len(problems) == 0:
            raise "Problem section contains no problems in chapter %s" % chapter['no']
        templates_dir = os.path.abspath(os.path.dirname(__file__) + "/../../epub/content")
        dir_name = uor.relative_url(settings.ROOT_URL, section['url'])
        section['content_file'] = os.path.join(settings.CONTENT_DIR, dir_name, 'problems.html')
        logger.debug("Collating problems for chapter %s in %s" % (chapter['no'], section['content_file']))
        shutil.copy(os.path.join(templates_dir, "problems.html.1"), section['content_file'])
        with open(section['content_file'], 'at') as fd:
            for problem in problems:
                with open(problem['content_file'], 'rt') as pfd:
                    logger.debug("Collating problem %s..." % (problem['no']))
                    problem_body = pfd.read()
                    problem_body = re.match(r'^.*?<body>(.*)</body>.*$', problem_body, re.S).group(1)
                    fd.write(problem_body)
                    fd.write("\n<br/><br/>\n")
            with open(os.path.join(templates_dir, "problems.html.2"), 'rt') as fd2:
                fd.write(fd2.read())
