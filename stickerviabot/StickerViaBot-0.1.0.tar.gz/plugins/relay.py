from StickerViaBot import utils
from StickerViaBot.plugin import InlineQueryPlugin
from StickerViaBot.default_pattern import P_FILE_ID


class Relay(InlineQueryPlugin):

    @property
    def cmd(self) -> str:
        return 'r'

    @property
    def pattern(self) -> str:
        return P_FILE_ID

    async def iter_inline_query_results(self, bot, query):
        match = query.matches[0]
        file_id = match.group('FILE_ID')  # 提取 FILE_ID
        if utils.check_sticker(file_id):  # 检查 FILE_ID 是否合理
            yield self.build_result_cached_sticker(file_id)