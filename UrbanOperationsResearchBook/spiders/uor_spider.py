'''
@author: rmahfoud
'''
import UrbanOperationsResearchBook as uor
import UrbanOperationsResearchBook.settings as settings
import scrapy
import os, shutil, re
from lxml import html, etree

class UORSpider(scrapy.Spider):
    name = settings.SPIDER_NAME
    allowed_domains = [settings.ALLOWED_DOMAIN]
    root_url = settings.ROOT_URL
    start_urls = [root_url]
    destination_dir = settings.CONTENT_DIR
    book = None
    
    def __init__(self, *args, **kwargs):
        shutil.rmtree(self.destination_dir, ignore_errors=True)
        os.makedirs(self.destination_dir)
        if 'book' in kwargs:
            self.book = kwargs['book']
        if not self.book:
            self.book = {'item_type': 'book'}
        self.chapters = dict()
        self.book['chapters'] = self.chapters
        return object.__init__(self, *args, **kwargs)

    def new_section(self): 
        return {'item_type': 'section'}

    def new_chapter(self):
        return {'item_type': 'chapter'}

    def parse(self, response):
        homepage = {'item_type': 'homepage'}
        self.book['homepage'] = homepage
        yield scrapy.Request(response.url, callback=self.parse_homepage, meta={'homepage': homepage})
        for href in response.xpath("//a[contains(@href,chapter)]/@href"):
            url = response.urljoin(href.extract())
            self.logger.debug("Crawling url %s" % url)
            yield scrapy.Request(url, callback=self.parse_chapter_contents)
        
    def parse_chapter_contents(self, response):
        # Chapter chapter_title
        chapter_spec = response.xpath("//table[1]/tr[1]/td[2]/font[1]/text()").extract()
        chapter_no = chapter_spec[1].strip().replace("Chapter ", "").replace(":", "")
        chapter_title = chapter_spec[2].strip()
        chapter = self.new_chapter()
        chapter['no'] = chapter_no
        chapter['title'] = chapter_title
        chapter['full_title'] = "Chapter %s: %s" % (chapter_no, chapter_title)
        chapter['contents_url'] = response.url
        chapter['sections'] = []
        self.chapters[int(chapter_no)] = chapter
        self.logger.debug("Chapter: %s, Title: %s" % (chapter_no, chapter_title))

        # Sections
        for row in response.xpath("//tr[descendant::a[not(starts-with(@href, '..'))]]"):
            a = row.xpath("td/a")
            if a:
                section = self.new_section()
                section_short_url = a.xpath("@href").extract_first().strip()
                section['url'] = uor.join_url(response.url, section_short_url)
                chapter['sections'].append(section)
                section_meta = {'section': section}
                if section_short_url == "problems2.html":
                    section['no'] = "problems"
                    section['title'] = "Problems"
                    section['full_title'] = "Chapter %s Problems" % chapter['no']
                    section['section_type'] = "problems"
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                elif section_short_url.startswith("problems"):
                    section['no'] = "problems"
                    section['title'] = "Problems"
                    section['full_title'] = "Chapter %s Problems" % chapter['no']
                    section['section_type'] = "problems"
                    yield scrapy.Request(section['url'], callback=self.parse_problems, meta=section_meta)
                elif section_short_url.startswith("references"):
                    section['no'] = "references"
                    section['title'] = "References"
                    section['full_title'] = "Chapter %s References" % chapter['no']
                    section['section_type'] = "references"
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                elif section_short_url.startswith("genref"):
                    section['no'] = "genref"
                    section['title'] = "General References"
                    section['full_title'] = "General References"
                    section['section_type'] = "general references"
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                else:
                    section['no'] = a.xpath("font/text()").extract_first().strip()
                    section['title'] = row.xpath("td[@bgcolor='ffddbb' or @bgcolor='bbbbff']/font/text()").extract_first().strip()
                    section['title'] = re.sub(r'\s+', ' ', section['title'])
                    section['full_title'] = "%s: %s" %(section['no'], section['title'])
                    section['section_type'] = "content"
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                self.logger.debug("Section %s, url: %s, title: %s" % (section['no'], section['url'], section['title']))
        yield chapter

    def cleanup_content(self, response):
        # Remove malformed comments
        body = re.sub(r'<!--.*?--!>', '', response.body)
        # Convert dirty HTML into well-formed xhtml
        doc = html.fromstring(body)
        body = etree.tostring(doc)
        # Add a namespace to the plain html element
        body = body.replace('<html>', '<html xmlns="http://www.w3.org/1999/xhtml">')
        # Add doctype
        DOCTYPE="""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
"""
        body = DOCTYPE + body
        # Insert reference to CSS
        body = body.replace("<head>", "<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"../UrbanOperationsResearch.css\" />")
        # Remove attributes of <body>
        body = re.sub(r'<body.*?>', '<body>', body)
        # Replace the styles of the main table
        body = re.sub(r'<table\s+border\s*=\s*"0"\s+width\s*=\s*"80%"\s+cellpadding\s*=\s*"10"\s*>', '<table class="main-table">', body)
        body = re.sub(r'<table\s+border\s*=\s*"0"\s+width\s*=\s*"(80%|732)"\s+cellpadding\s*=\s*"10"\s*>', '<table class="main-table">', body)
        # Replace the styles of other common kind of tables
        body = re.sub(r'<table\s+width\s*=\s*"100%"\s*>', '<table class="fullwidth-table">', body)
        # Center images using CSS instead of <centers> tag which is disallowed in XHTML.. add an alt while at it...
        body = re.sub(r'<center>\s*<img (.*?)/>\s*</center>', r'<img class="block-centered" \1 />', body)
        body = re.sub(r'<center>\s*((?:<br\s*/>\s*)*)<img (.*?)/>\s*</center>', r'\1<img class="block-centered" \2 />', body)
        body = re.sub(r'<center>\s*<p>\s*<img (.*?)/>\s*</p>\s*</center>', r'<img class="block-centered" \1 />', body)
        body = re.sub(r'<center>\s*<pre>\s*<img (.*?)/>\s*</pre>\s*</center>', r'<img class="block-centered" \1 />', body)
        # Remove horizontal
        body = re.sub(r'<hr\s*/>', '', body)
        # Remove navigation buttons
        body = re.sub(r'<a .*?>\s*<img\s*src="images/next.gif" .*?</a>', '', body);
        body = re.sub(r'<a .*?>\s*<img\s*src="images/contents.gif".*?</a>', '', body);
        body = re.sub(r'(<br\s*/>\s*)*\s*<p>\s*(<br\s*/>\s*)*\s*<a .*?>\s*<img\s*src="images/previous.gif".*?</a>\s*(<br\s*/>\s*)*\s*</p>\s*(<br\s*/>\s*)*', '', body);
        
        return response.replace(body=body)

    def parse_section_contents(self, response):
        section = response.meta['section']
        self.logger.debug("Parsing content of %s" % response.url)

        # Remove "extra" stuff and convert into valid xhtml
        response = self.cleanup_content(response)
        # Save to file name matchine url
        file_name = uor.relative_url(self.root_url, response.url)
        self.logger.debug("Saving body of %s to %s" % (response.url, file_name))
        section['content_file'] = self.save_to_file(file_name, response.body)
        # Download images
        section['file_urls'] = [uor.join_url(response.url, url) for url in response.xpath('//table//img/@src').extract()]
        yield section

    def parse_homepage(self, response):
        homepage = response.meta['homepage']
        self.logger.debug("Parsing content of home page %s" % response.url)
        # Discard content but only download resources
        homepage['file_urls'] = [uor.join_url(response.url, url) for url in response.xpath('//table//img/@src').extract()]
        yield homepage

    def parse_problems(self, response):
        section = response.meta['section']
        self.logger.debug("Parsing problems for section: %s" % section)

        file_name = uor.relative_url(self.root_url, response.url)
        self.logger.debug("Saving body of %s to %s" % (response.url, file_name))
        section['content_file'] = self.save_to_file(file_name, response.body)
        yield section

    def save_to_file(self, file_name, body):
        file_name = os.path.join(self.destination_dir, file_name)
        if os.path.isdir(file_name) or file_name.endswith('/'):
            file_name = os.path.join(file_name, 'index.html')
        self.logger.debug("Writing file %s" % file_name)
        dirname = os.path.dirname(file_name)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(file_name, 'wb') as f:
            f.write(body)

        return file_name
