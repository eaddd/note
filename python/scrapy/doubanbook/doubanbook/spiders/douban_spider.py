import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.selector import Selector
from doubanbook.items import DoubanbookItem, DoubanSubjectItem
import logging
log = logging.getLogger(__name__)


class DoubanSpiderSpider(CrawlSpider):
    name = "douban_spider"
    allowed_domains = ["douban.com"]
    start_urls = ["https://book.douban.com/tag/"]
    rules = [
        Rule(sle(allow=("/subject/\d+/$")), callback='parseSubject'),
        Rule(sle(allow=("/tag/[^/]+$")), callback='parseTag', follow=True)
    ]

    def parseTag(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # log.info('parsed ' + str(response))
        pass

    def parseSubject(self, response):
        log.info('parseSubject ' + str(response))
        subjects = []
        sel = Selector(response)
        sites = sel.css('#wrapper')
        for site in sites:
            subject = DoubanSubjectItem()
            subject['title'] = site.css('h1 span::text').extract()
            subject['link'] = response.url
            subject['info'] = site.xpath(
                '//div[@id="info"]/descendant-or-self::*/text()').extract()
            subject['rate'] = site.xpath(
                '//strong[@class="ll rating_num "]/text()').extract()
            subject['votes'] = site.xpath(
                '//span[@property="v:votes"][1]').extract()
            subject['author_intro'] = site.xpath(
                '//div[@class="indent"]//div/div[@class="intro"]/text()').extract()
            subject['content_intro'] = site.css(
                '#link-report .intro p::text').extract()
            subjects.append(subject)
            log.info('data:' + str(subject))
        return subjects

    def process_request(self, request):
        log.info('process ' + str(request))
        return request

    def closed(self, reason):
        log.info("DoubanBookSpider Closed:" + reason)
