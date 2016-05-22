#! /usr/bin/python
import sys
sys.path.append('../UrbanOperationsResearchBook')

import UrbanOperationsResearchBook.settings as settings
from UrbanOperationsResearchBook.epub.uor_generators import UORContentsGenerator
from UrbanOperationsResearchBook.epub.uor_generators import UORNCXGenerator
from UrbanOperationsResearchBook.epub.uor_generators import UOROPFGenerator
from UrbanOperationsResearchBook.epub.uor_problems import UORProblemsGenerator
import shutil, json, os

if __name__ == '__main__':
    # Read the JSON from the file
    with open(os.path.join(settings.ROOT_DIR, "book.json"), "rt") as fd:
        book = json.load(fd)
    templates_dir = os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0])) + "/../epub/content")

    # The problems
    problemgen = UORProblemsGenerator(book)
    problemgen.generateProblemsContent()
    
    # The HTML table of contents
    contents_file = os.path.join(settings.CONTENT_DIR, "contents.html")
    shutil.copy(os.path.join(templates_dir, "contents.html.1"), contents_file)
    contentsgen  = UORContentsGenerator(book)
    with open(contents_file, 'at') as fd:
        contentsgen.generateChapters(fd)
        with open(os.path.join(templates_dir, "contents.html.2"), 'rt') as fd2:
            fd.write(fd2.read())

    # The NCX File    
    ncx_file = os.path.join(settings.CONTENT_DIR, "toc.ncx")
    shutil.copy(os.path.join(templates_dir, "toc.ncx.1"), ncx_file)
    ncxgen  = UORNCXGenerator(book)
    with open(ncx_file, 'at') as fd:
        # The core navMap
        ncxgen.generateNavMap(fd)
        with open(os.path.join(templates_dir, "toc.ncx.2"), 'rt') as fd2:
            fd.write(fd2.read())

        # The apgeList
        ncxgen.generatePageList(fd)
        with open(os.path.join(templates_dir, "toc.ncx.3"), 'rt') as fd2:
            fd.write(fd2.read())

    # The OPF file
    opf_file = os.path.join(settings.CONTENT_DIR, "UrbanOperationsResearch.opf")
    shutil.copy(os.path.join(templates_dir, "UrbanOperationsResearch.opf.1"), opf_file)
    opfgen = UOROPFGenerator(book)        
    with open(opf_file, 'at') as fd:
        # OPF manifest entries
        opfgen.addManifestEntries(fd)
        with open(os.path.join(templates_dir, "UrbanOperationsResearch.opf.2"), 'rt') as fd2:
            fd.write(fd2.read())
    
        # OPF spine entries
        opfgen.addSpineEntries(fd)
        with open(os.path.join(templates_dir, "UrbanOperationsResearch.opf.3"), 'rt') as fd2:
            fd.write(fd2.read())
