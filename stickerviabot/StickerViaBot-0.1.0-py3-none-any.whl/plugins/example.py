from StickerViaBot import utils
from StickerViaBot.plugin import InlineQueryPlugin


class Example(InlineQueryPlugin):

    @property
    def cmd(self) -> str:
        return ''

    @property
    def pattern(self) -> str:
        return ''

    @property
    def inline_pattern(self) -> str:
        return r'example'

    async def iter_inline_query_results(self, bot, query):
        file_id = 'CAACAgUAAxkBAAIaQGKrcBkVuEWJ_o0_AUA_fkVOhmgvAAKYBAACGrRAV733Cay8xtigHgQ'
        if utils.check_sticker(file_id):
            yield self.build_result_cached_sticker(file_id)