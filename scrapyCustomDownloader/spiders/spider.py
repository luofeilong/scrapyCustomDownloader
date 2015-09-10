__author__ = 'dragon'


import time

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapyCustomDownloader.items import ScrapycustomdownloaderItem
from scrapy.spider import Spider


class MininovaSpider(CrawlSpider):
    name = 'baidu'

    start_urls = ["http://yuedu.baidu.com/book/list/0?od=0&show=1&pn=0"]
    rules = [Rule(SgmlLinkExtractor(allow=('/ebook/[^/]+fr=booklist')), callback='parse_torrent'), Rule(SgmlLinkExtractor(allow=('/book/list/[^/]+pn=[^/]+', )), follow=True)]

    def parse_torrent(self, response):
        x = HtmlXPathSelector(response)
        torrent = ScrapycustomdownloaderItem()

        torrent['url'] = response.url
        torrent['name'] = ""
        torrent['price'] = ""
        torrent['memprice'] = ""
        torrent['press'] = ""
        torrent['publication'] = ""
        torrent['author'] = ""
        torrent['desc'] = ""
        torrent['belong'] = ""

        strlist = x.select("//h1/@title").extract()
        if len(strlist) > 0:
            torrent['name'] = strlist[0]


        #print response.url+"    "+torrent['name']

        strlist = x.select("//div[@class='doc-info-price']//span[@class='txt-now-price-num']/text()").extract()
        if len(strlist) > 0:
            torrent['price'] = strlist[0]

        strlist = x.select("//div[contains(@class, 'privilege-price')]/span[contains(@class, 'txt-old-price')]/text()").extract()
        if len(strlist) > 0:
            torrent['memprice'] = strlist[0]

        strlist = x.select("//ul[@class='doc-info-org']/li/a/text()").extract()

        count = len(strlist)
        if count > 0:
            torrent['author'] = strlist[0]

        if count > 1:
            torrent['publication'] = strlist[1]

        if count > 2:
            torrent['press'] = strlist[2]


        strlist = x.select("//div[@class='des-content']/p/text()").extract()
        if len(strlist) > 0:
            torrent['desc'] = strlist[0]

        strlist = x.select("//li/a[contains(@data-logsend, 'send')]/text()").extract()

        belong = ""
        index = 0
        for str in strlist:
            index += 1
            if index <= 1:
                continue

            if len(belong) <= 0:
                belong += str
            else:
                belong += "->"+str

        torrent['belong'] = belong

        #print belong

        self.log(torrent['url']+"    "+torrent['name']+"    " + torrent['author'])
        return torrent