'''
@author: rmahfoud
'''

import UrbanOperationsResearchBook as uor

class UORXmlGenerator():
    MISSING_CONTENT_FILE = "#"
    current_indent = 0

    def __init__(self, book, *args, **kwargs):
        self.book = book
    
    def write_line(self, outfd, line):
        outfd.write(' ' * self.current_indent)
        outfd.write(line)
        outfd.write("\n")
        
    def relative_url(self, path):
        return uor.relative_url(self.book['base_dir'], path)
    
    def get_chapter_content_file(self, chapter):
        if 'content_file' in chapter:
            return chapter['content_file']
        else:
            return chapter['sections'][0]['content_file']
 
    def get_section_id(self, chapter_no, section):
        return "chapter%s_section%s" %(chapter_no, section['no'])

    def is_sub_section(self, section, next_section):
        current_no = section['no']
        next_no = next_section['no']
        return next_no.startswith(current_no + ".")

    def get_section_content(self, section):
        missing_indicator = ""
        if not 'content_file' in section:
            missing_indicator = " (missing)"
            content_file = self.MISSING_CONTENT_FILE
        else:
            content_file = section['content_file']
        return content_file, missing_indicator

    def all_sections_minus_first(self, chapter):
        first = True
        for section in chapter['sections']:
            if not first:
                yield section
            else:
                first = False

class UORContentsGenerator(UORXmlGenerator):
    depth = 1
    first_section = False

    def __init__(self, book, *args, **kwargs):
        self.book = book
    
    def generateChapters(self, outfd):
        self.current_indent = 0
        for chapter_no in sorted(self.book['chapters'].keys()):
                self.generateChapter(outfd, self.book['chapters'][chapter_no])

    def generateChapter(self, outfd, chapter):
        self.current_indent = 0
        self.depth = 1
        section = chapter['sections'][0]
        content_file, missing_indicator = self.get_section_content(section)
        self.write_line(outfd, \
                    '<h%d class="contents"><span class="content-section_no">Chapter %s</span> <a href="%s">%s</a></h%d>' % \
                    (self.depth, chapter['no'], self.relative_url(content_file), chapter['title'], self.depth))
        section_index = 1
        while section_index < len(chapter['sections']):
            section_index = self.generateSection(outfd, chapter, section_index)
    
    def generateSection(self, outfd, chapter, section_index):
        self.current_indent += 4
        self.depth += 1
        section = chapter['sections'][section_index]
        content_file, missing_indicator = self.get_section_content(section)
        if section['section_type'] == 'content':
            section_no = section['no']
            section_title = section['title']
        else:
            section_no = ''
            section_title = section['full_title']
        self.write_line(outfd, \
                    '<h%d class="contents"><span class="content-section_no">%s</span> <a href="%s">%s%s</a></h%d>' % \
                    (self.depth, section_no, self.relative_url(content_file), section_title, missing_indicator, self.depth))
        section_index = section_index + 1
        while section_index < len(chapter['sections']):
            if self.is_sub_section(section, chapter['sections'][section_index]):
                section_index = self.generateSection(outfd, chapter, section_index)
            else:
                break
        self.current_indent -= 4
        self.depth -= 1
        return section_index


class UORNCXGenerator(UORXmlGenerator):
    """
        See: http://www.daisy.org/z3986/2005/Z3986-2005.html#NCX
    """
    depth = 1
    first_section = False

    def __init__(self, book, *args, **kwargs):
        self.book = book
    
    def generateNavMap(self, outfd):
        self.current_indent = 8
        for chapter_no in sorted(self.book['chapters'].keys()):
            self.generateChapterNavPoint(outfd, self.book['chapters'][chapter_no])

    def generateChapterNavPoint(self, outfd, chapter):
        self.depth = 1
        section = chapter['sections'][0]
        content_file, missing_indicator = self.get_section_content(section)
        self.write_line(outfd, "<navPoint class=\"h%d\" id=\"%s\">" % (self.depth, self.get_section_id(chapter['no'], section)))
        self.write_line(outfd, "    <navLabel><text>%s</text></navLabel>" % chapter['full_title'])
        self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(content_file))

        section_index = 1
        while section_index < len(chapter['sections']):
            section_index = self.addSectionNavPoint(outfd, chapter, section_index)
        
        self.write_line(outfd, "</navPoint>")

    def addSectionNavPoint(self, outfd, chapter, section_index):
        self.current_indent += 4
        self.depth += 1
        section = chapter['sections'][section_index]
        content_file, missing_indicator = self.get_section_content(section)
        self.write_line(outfd, "<navPoint class=\"h%d\" id=\"%s\">" % (self.depth, self.get_section_id(chapter['no'], section)))
        self.write_line(outfd, "    <navLabel><text>%s%s</text></navLabel>" % (section['full_title'], missing_indicator))
        self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(content_file))
        section_index = section_index + 1
        while section_index < len(chapter['sections']):
            if self.is_sub_section(section, chapter['sections'][section_index]):
                section_index = self.addSectionNavPoint(outfd, chapter, section_index)
            else:
                break
        self.write_line(outfd, "</navPoint>")
        self.current_indent -= 4
        self.depth -= 1
        return section_index
    
    def generatePageList(self, outfd):
        self.current_indent = 8
        for chapter_no in sorted(self.book['chapters'].keys()):
            for section in self.book['chapters'][chapter_no]['sections']:
                if section['section_type'] != 'content' and 'content_file' in section:
                    self.write_line(outfd, "<pageTarget class=\"h2\" id=\"page_%s\" type=\"normal\">" % self.get_section_id(chapter_no, section))
                    self.write_line(outfd, "    <navLabel><text>%s</text></navLabel>" % section['full_title'])
                    self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(section['content_file']))
                    self.write_line(outfd, "</pageTarget>")
                    

class UOROPFGenerator(UORXmlGenerator):

    def __init__(self, book, *args, **kwargs):
        self.book = book

    def addManifestEntries(self, outfd):
        self.current_indent = 8
        for chapter_no in sorted(self.book['chapters'].keys()):
            for section in self.book['chapters'][chapter_no]['sections']:
                if 'content_file' in section:
                    self.write_line(outfd, "<item id=\"%s\" href=\"%s\" media-type=\"application/xhtml+xml\" />" \
                                    % (self.get_section_id(chapter_no, section), self.relative_url(section['content_file'])))
                

    def addSpineEntries(self, outfd):
        self.current_indent = 8
        for chapter_no in sorted(self.book['chapters'].keys()):
            for section in self.book['chapters'][chapter_no]['sections']:
                if 'content_file' in section:
                    self.write_line(outfd, "<itemref idref=\"%s\" />" % self.get_section_id(chapter_no, section))
