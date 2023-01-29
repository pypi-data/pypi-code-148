from itemadapter import ItemAdapter
import httpx

class ScrapyTutorialPipeline:
    def process_item(self, item, spider):
        return item


class ScrapyPipeLine2:
    def process_item(self, item, spider):
        callback_url = spider.settings.get("MTX_ITEM_CALLBACK_URL")
        if callback_url:
            print(f"callback_url: {callback_url}, item: {item}" )
            httpx.post(callback_url,data=item)
        return item 