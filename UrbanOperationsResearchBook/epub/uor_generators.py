'''
@author: rmahfoud
'''

import UrbanOperationsResearchBook as uor

class UORXmlGenerator():
    MISSING_CONTENT_FILE = "."
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

        
class UORNCXGenerator(UORXmlGenerator):
    depth = 1

    def __init__(self, book, *args, **kwargs):
        self.book = book
    
    def generateNavMap(self, outfd):
        self.current_indent = 8
        for chapter_no in sorted(self.book['chapters'].keys()):
            self.generateChapterNavPoint(outfd, self.book['chapters'][chapter_no])

    def generateChapterNavPoint(self, outfd, chapter):
        self.write_line(outfd, "<navPoint class=\"h%d\" id=\"chapter%s\">" % (self.depth, chapter['no']))
        self.write_line(outfd, "    <navLabel><text>%s</text></navLabel>" % chapter['full_title'])
        self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(self.get_chapter_content_file(chapter)))
        if chapter['no'] != 0:
            section_index = 0
            while section_index < len(chapter['sections']):
                section_index = self.addSectionNavPoint(outfd, chapter, section_index)
        self.write_line(outfd, "</navPoint>")
    

    def isSubSection(self, section, next_section):
        current_no = section['no']
        next_no = next_section['no']
        return next_no.startswith(current_no + ".")
    
    def addSectionNavPoint(self, outfd, chapter, section_index):
        self.current_indent += 4
        self.depth += 1
        section = chapter['sections'][section_index]
        self.write_line(outfd, "<navPoint class=\"h%d\" id=\"%s\">" % (self.depth, self.get_section_id(chapter['no'], section)))
        missing_indicator = ""
        if not 'content_file' in section:
            missing_indicator = " (missing)"
            section['content_file'] = self.MISSING_CONTENT_FILE
        self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(section['content_file']))
        self.write_line(outfd, "    <navLabel><text>%s%s</text></navLabel>" % (section['full_title'], missing_indicator))
        section_index = section_index + 1
        while section_index < len(chapter['sections']):
            if self.isSubSection(section, chapter['sections'][section_index]):
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
                if section['section_type'] != 'content':
                    self.write_line(outfd, "<pageTarget class=\"h2\" id=\"%s\" type=\"normal\">" % self.get_section_id(chapter_no, section))
                    self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(section['content_file']))
                    self.write_line(outfd, "    <navLabel><text>%s</text></navLabel>" % section['full_title'])
                    self.write_line(outfd, "</pageTarget>")
                    

class UOROPFGenerator(UORXmlGenerator):

    def __init__(self, book, *args, **kwargs):
        self.book = book

    def addManifestEntries(self, outfd):
        self.current_indent = 8
        for chapter_no in sorted(self.book['chapters'].keys()):
            if chapter_no == 0:
                continue
            for section in self.book['chapters'][chapter_no]['sections']:
                self.write_line(outfd, "<item id=\"%s\" href=\"%s\" media-type=\"application/xhtml+xml\" />" \
                                % (self.get_section_id(chapter_no, section), self.relative_url(section['content_file'])))
                

    def addSpineEntries(self, outfd):
        self.current_indent = 8
        for chapter_no in sorted(self.book['chapters'].keys()):
            if chapter_no == 0:
                continue
            for section in self.book['chapters'][chapter_no]['sections']:
                self.write_line(outfd, "<itemref idref=\"%s\" />" % self.get_section_id(chapter_no, section))
