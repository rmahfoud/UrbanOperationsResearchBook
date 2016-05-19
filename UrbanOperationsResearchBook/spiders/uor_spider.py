'''
@author: rmahfoud
'''
import UrbanOperationsResearchBook as uor
import UrbanOperationsResearchBook.settings as settings
import scrapy
import os, shutil, re

class UORSpider(scrapy.Spider):
    name = settings.SPIDER_NAME
    allowed_domains = [settings.ALLOWED_DOMAIN]
    root_url = settings.ROOT_URL
    start_urls = [root_url]
    destination_dir = settings.CONTENT_DIR
    
    def __init__(self, *args, **kwargs):
        if os.path.isdir(self.destination_dir):
            shutil.rmtree(self.destination_dir)
        os.makedirs(self.destination_dir)
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
        chapter = self.new_chapter()
        chapter['no'] = 0
        chapter['title'] = 'Home Page'
        chapter['full_title'] = 'Home Page'
        chapter['url'] = response.url
        chapter['sections'] = []
        section_meta = {'section': chapter}
        yield scrapy.Request(response.url, callback=self.parse_section_contents, meta=section_meta)
        self.chapters[0] = chapter
        yield chapter
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

    def parse_section_contents(self, response):
        section = response.meta['section']
        self.logger.debug("Parsing content of %s" % response.url)

        # Remove malformed comments
        response = response.replace(body=response.body.replace("<!--table--!>", ""))
        # Remove anything before and after the horizontal lines
        body = re.sub(r'(?is)(^.*<body[^>]*>).*?<hr>(.*)<hr>.*(</body>.*$)', r'\1\2\3', response.body)
        # Save to file name matchine url
        file_name = uor.relative_url(self.root_url, response.url)
        self.logger.debug("Saving body of %s to %s" % (response.url, file_name))
        section['content_file'] = self.save_to_file(file_name, body)
        # Download images
        section['file_urls'] = [uor.join_url(response.url, url) for url in response.xpath('//table//img/@src').extract()]
        yield section

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
