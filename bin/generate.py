#! /usr/bin/python
import sys
sys.path.append('../UrbanOperationsResearchBook')

import UrbanOperationsResearchBook.settings as settings
from UrbanOperationsResearchBook.epub.uor_generators import UORNCXGenerator
from UrbanOperationsResearchBook.epub.uor_generators import UOROPFGenerator
import shutil, json, os

if __name__ == '__main__':
    content_dir = os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0])) + "/../epub/content")
    ncx_file = os.path.join(settings.BOOK_FILES, "toc.ncx")
    shutil.copy(os.path.join(content_dir, "toc.ncx.1"), ncx_file)

    # Read the JSON from the file
    with open(os.path.join(settings.ROOT_DIR, "book.json"), "rt") as fd:
        result_book = json.load(fd)
    ncxgen  = UORNCXGenerator(result_book)
    with open(ncx_file, 'at') as fd:
        # The core navMap
        ncxgen.generateNavMap(fd)
        with open(os.path.join(content_dir, "toc.ncx.2"), 'rt') as fd2:
            fd.write(fd2.read())

        # The apgeList
        ncxgen.generatePageList(fd)
        with open(os.path.join(content_dir, "toc.ncx.3"), 'rt') as fd2:
            fd.write(fd2.read())

    opf_file = os.path.join(settings.BOOK_FILES, "UrbanOperationsResearch.opf")
    shutil.copy(os.path.join(content_dir, "UrbanOperationsResearch.opf.1"), opf_file)
    opfgen = UOROPFGenerator(result_book)        
    with open(opf_file, 'at') as fd:
        # OPF manifest entries
        opfgen.addManifestEntries(fd)
        with open(os.path.join(content_dir, "UrbanOperationsResearch.opf.2"), 'rt') as fd2:
            fd.write(fd2.read())
    
        # OPF spine entries
        opfgen.addSpineEntries(fd)
        with open(os.path.join(content_dir, "UrbanOperationsResearch.opf.3"), 'rt') as fd2:
            fd.write(fd2.read())
    