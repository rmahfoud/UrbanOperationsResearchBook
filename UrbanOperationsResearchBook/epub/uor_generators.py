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
        if chapter['no'] != 0:
            main_section = chapter['sections'][0]['content_file']
        else:
            main_section = chapter['content_file']
        self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(main_section))
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
        self.write_line(outfd, "<navPoint class=\"h%d\" id=\"chapter%s_section%s\">" % (self.depth, chapter['no'], section['no']))
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
                    self.write_line(outfd, "<pageTarget class=\"h2\" id=\"chapter%s_section%s\" type=\"normal\">" % (chapter_no, section['no']))
                    self.write_line(outfd, "    <content src=\"%s\" />" % self.relative_url(section['content_file']))
                    self.write_line(outfd, "    <navLabel><text>%s</text></navLabel>" % section['full_title'])
                    self.write_line(outfd, "</pageTarget>")
