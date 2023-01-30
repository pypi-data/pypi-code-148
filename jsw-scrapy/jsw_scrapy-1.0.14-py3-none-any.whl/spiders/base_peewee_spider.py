import scrapy
import jsw_nx as nx


class BasePeeweeSpider:
    handle_httpstatus_list = [400]
    ua_pc = 'Mozilla/5.0 zgrab/0.x'
    ua_mobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) By aric.zheng/0.x'
    support_crawling = False

    @classmethod
    def get_un_crawled(cls, **kwargs):
        entity_class = kwargs.get('entity_class')
        limit = kwargs.get('limit', None)
        if limit:
            records = entity_class.select().where(entity_class.is_crawled == False).limit(limit)
        else:
            records = entity_class.select().where(entity_class.is_crawled == False)
        return records

    @classmethod
    def update_crawled(cls, **kwargs):
        record = kwargs.get('record')
        crawled = kwargs.get('crawled', 'is_crawled')
        setattr(record, crawled, True)
        record.save()

    @classmethod
    def noop_request(cls):
        yield scrapy.Request(url="https://www.baidu.com", callback=nx.noop_scrapy_parse)
