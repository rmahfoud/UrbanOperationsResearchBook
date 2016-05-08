'''
@author: rmahfoud
'''

import scrapy
import os, shutil, re, urlparse

class UORSpider(scrapy.Spider):
    name = "uor"
    allowed_domains = ["web.mit.edu"]
    root_url = "http://web.mit.edu/urban_or_book/www/book/"
    start_urls = [root_url]
    destination_dir = "/tmp/" + name + "/"
    chapters = dict()

    def __init__(self, *args, **kwargs):
        if os.path.isdir(self.destination_dir):
            shutil.rmtree(self.destination_dir)
        os.makedirs(self.destination_dir)
        return object.__init__(self, *args, **kwargs)

    def parse(self, response):
        for href in response.xpath("//a[contains(@href,chapter)]/@href"):
            url = response.urljoin(href.extract())
            self.logger.debug("Crawling url %s" % url)
            yield scrapy.Request(url, callback=self.parse_chapter_contents)
        #self.save_file("index.html", response.body)
        print self.chapters

    def parse_chapter_contents(self, response):
        # Chapter chapter_title
        chapter_spec = response.selector.xpath("//table[1]/tr[1]/td[2]/font[1]/text()").extract()
        chapter_no = chapter_spec[1].strip().replace("Chapter ", "").replace(":", "")
        chapter_title = chapter_spec[2].strip()
        chapter = dict()
        chapter['no'] = chapter_no
        chapter['title'] = chapter_title
        chapter['contents_page'] = response.url
        chapter['sections'] = []
        self.chapters[chapter_no] = chapter
        self.logger.debug("Chapter: %s, Title: %s" % (chapter_no, chapter_title))

        # Sections
        for row in response.xpath("//tr[descendant::a[not(starts-with(@href, '..'))]]"):
            a = row.xpath("td/a")
            if a:
                section = dict()
                section_short_url = a.xpath("@href").extract_first().strip()
                section['url'] = self.get_full_url(response.url, section_short_url)
                chapter['sections'].append(section)
                section_meta = {'section': section}
                if section_short_url == "problems2.html":
                    section['no'] = "problems"
                    section['title'] = "Problems"
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                elif section_short_url.startswith("problems"):
                    section['no'] = "problems"
                    section['title'] = "Problems"
                    yield scrapy.Request(section['url'], callback=self.parse_problems, meta=section_meta)
                elif section_short_url.startswith("references"):
                    section['no'] = "references"
                    section['title'] = "References"
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                elif section_short_url.startswith("genref"):
                    section['no'] = "genref"
                    section['title'] = "General References"
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                else:
                    section['no'] = a.xpath("font/text()").extract_first().strip()
                    section['title'] = row.xpath("td[@bgcolor='ffddbb' or @bgcolor='bbbbff']/font/text()").extract_first().strip()
                    section['title'] = re.sub(r'\s+', ' ', section['title'])
                    yield scrapy.Request(section['url'], callback=self.parse_section_contents, meta=section_meta)
                self.logger.debug("Section %s, url: %s, title: %s" % (section['no'], section['url'], section['title']))
        yield chapter

    def parse_section_contents(self, response):
        self.logger.debug("Parsing content of %s" % response.url)
        # Remove anything before and after the horizontal lines
        body = re.sub(r'(?is)(^.*<body[^>]*>).*?<hr>(.*)<hr>.*(</body>.*$)', r'\1\2\3', response.body)
        # Save to file name matchine url
        file_name = self.get_file_name(response.url)
        self.logger.debug("Saving body of %s to %s" % (response.url, file_name))
        return self.save_to_file(file_name, body)

    def parse_problems(self, response):
        section = response.meta['section']
        self.logger.debug("Parsing prolems for section: %s" % section)
        pass

    def cleanup_page(self, url):
        pass
    
    def save_contents(self, section, url):
        pass
    
    def save_image(self, url):
        pass

    def get_full_url(self, referrer, url):
        if referrer:
            url = urlparse.urljoin(referrer, url)
        return url

    def get_file_name(self,  url):
        return re.sub(r'^' + self.root_url, '',  url)
    
    def save_to_file(self, file_name, body):
        file_name = os.path.join(self.destination_dir, file_name)
        self.logger.debug("Writing file %s" % file_name)
        dirname = os.path.dirname(file_name)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(file_name, 'wb') as f:
            f.write(body)

