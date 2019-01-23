# 京东商城评论爬虫
# https://blog.csdn.net/sinat_33741547/article/details/78658321
import scrapy
import os

class CommentSpider(scrapy.Spider):
    name = 'comment'
    # 评论地址
    CM_URL = 'https://club.jd.com/repay/6162164_0092954c-c357-4e9d-b5df-24fcf6a6ea50_1.html'
    allowed_domains = []
    start_urls = ['http://www.jd.com/']

    def parse(self, response):
        path = os.path.join(os.getcwd(), 'data', 'identity.txt')
        fr = open(path, 'r')
        urls = [(CM_URL.format(i.strip(), s, 0), s) for i in fr.readlines() for _, s in SC_MAPS.items()]
        for url, score in urls:
            yield Request(url, meta={'page': 0, 'score': score}, callback=self.parse_comment)

    def parse_comment(self, response):
        item = JdItem()
        meta = response.meta
        response_json = demjson.decode(txt=response.text, encoding='utf-8')
        if meta['page'] < int(response_json['maxPage']) and meta['page'] < 100:
            meta['page'] += 1
            url = u'='.join(response._url.split(u'=')[:-1]) + u'=' + str(meta['page'])
            yield Request(url, meta=meta, callback=self.parse_comment)
        for c in response_json['comments']:
            content = ''.join(c['content']).strip().replace(u'\n', u'').replace(u'\r', u'').encode('utf-8')
            item['info'] = '{} {}'.format(meta['score'], content)
            yield item