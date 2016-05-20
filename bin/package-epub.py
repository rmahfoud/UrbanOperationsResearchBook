#! /usr/bin/python
import sys
import os
import zipfile
import shutil

sys.path.append('../UrbanOperationsResearchBook')
import UrbanOperationsResearchBook as uor
import UrbanOperationsResearchBook.settings as settings


if __name__ == '__main__':
    epub_source = settings.BOOK_DIR
    epub_templates = os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0])) + "/../epub")

    # mimetype & co
    shutil.copy(os.path.join(epub_templates, "mimetype"), os.path.join(epub_source, "mimetype"))
    meta_inf = os.path.join(epub_source, "META-INF")
    shutil.rmtree(meta_inf, ignore_errors=True)
    shutil.copytree(os.path.join(epub_templates, "META-INF"), meta_inf)
    shutil.copy(os.path.join(epub_templates, "content/UrbanOperationsResearch.css"), os.path.join(epub_source, "content/UrbanOperationsResearch.css"))

    epubfile_name = os.path.join(settings.ROOT_DIR, "uor.epub")
    epubfile = zipfile.ZipFile(epubfile_name, "w", zipfile.ZIP_DEFLATED, False)
    epubfile.debug = 3
    def add_file(file, compression=zipfile.ZIP_DEFLATED):
        epubfile.write(file, uor.relative_url(epub_source, file), compression)
    
    def add_dir(dir, compression=zipfile.ZIP_DEFLATED):
        for file in os.listdir(dir):
            full_path = os.path.join(dir, file)
            if os.path.isfile(full_path):
                add_file(full_path, compression)
            elif os.path.isdir(full_path):
                add_dir(full_path, compression)
    add_file(os.path.join(epub_source, "mimetype"), zipfile.ZIP_STORED)
    add_dir(os.path.join(epub_source, "META-INF"))
    add_dir(os.path.join(epub_source, "content"))
    epubfile.close()
