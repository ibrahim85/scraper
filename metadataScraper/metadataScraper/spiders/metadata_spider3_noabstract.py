# Metadata Scraper v3
# Scrapes metadata URLs from http://hydro10.sdsc.edu/metadata/ScienceBase_WAF_dump/
# Passes URLs to metadata scraper to get links under <gmd:URL> tag, title, author
# Run in terminal with scrapy crawl metadata
# SAMPLE OUTPUT can be found in s3output.json
# Date: June 29 2015
# Quirk: the TO PARENT DIRECTORY url also gets scraped from hydro10 resulting in
# an empty entry in the output json {"title": [], "author": []} because it
# doesn't link to an xml document but rather goes up a level in the directory

# 7/14/15: Triple quotes at beginning and end only; took out fluff

'''
import scrapy
from scrapy import signals
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import json
import time
# import logging
# See http://doc.scrapy.org/en/latest/topics/selectors.html

from metadataScraper.items import MetadatascraperItem
# A class from items.py; copied from tutorial

timestamp = time.strftime("%Y-%m-%d_%H%M%S")
filename = "SPIDER_3_METADATA_NO_ABSTRACT.json"
# filename = "metadata_" + timestamp + ".json"
f = open(filename, 'w')

# logger = logging.getLogger(__name__)

class MetadataSpider(scrapy.Spider):
    name = "sciencebase-noabstract"
    allowed_domains = ["hydro10.sdsc.edu"]
    start_urls = [
        "http://hydro10.sdsc.edu/metadata/ScienceBase_WAF_dump/"
    ]

    def parse(self, response):
        # Finds all links to metadata XMLs on hydro10 directory page

        for href in response.xpath("//a/@href"):
            url = response.urljoin(href.extract())
            # Joins href's output (/metadata/Scien.../[id].xml) to
            # hydro10.sdsc.edu to make a valid link
            yield scrapy.Request(url, callback=self.parse_metadata)
            # Passes links to parse_metadata() function

    def parse_metadata(self, response):
        # Finds all links under <gmd:URL> XML tag in metadata documents
        # in addition to author and title

        item = MetadatascraperItem()
        response.selector.remove_namespaces()
        # See http://doc.scrapy.org/en/latest/topics/selectors.html#removing-namespaces
        # xpath had issues because the metadata documents contained namespaces
        # e.g. <gmd:URL> instead of <URL>
        # response.xpath("//gmd:URL") doesn't work; look into later
        # remove_namespaces() takes out gmd: so xpath('//URL') works
        if response.xpath('//abstract/CharacterString/text()').extract() == [u'REQUIRED FIELD']:
            item['title'] = response.xpath('//title/CharacterString/text()').extract()
            item['author'] = response.xpath('//individualName/CharacterString/text()').extract()
            for sel in response.xpath('//linkage'):
                item['link'] = response.xpath('//URL/text()').extract()
                # Finds text in multiple <gmd:URL> tags (the links)
                # Adds each of them to link in items.py
            json.dump(dict(item), f)
            f.write("\n")
'''
