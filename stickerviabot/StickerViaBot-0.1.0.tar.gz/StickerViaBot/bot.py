import asyncio
import logging

import pluginlib
from pyrogram import Client, filters
from pyrogram.handlers import InlineQueryHandler, MessageHandler
from pyrogram.types import Message, InlineQuery, \
    InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton

from .utils import Utils


SESSION_NAME = 'StickerBot'
CACHE_TIME = 60


class Bot(Client, Utils):

    async def run_in_executor(self, func, *args, **kwargs):
        return await self.loop.run_in_executor(
            executor=None,
            func=func, *args, **kwargs
        )


def create_bot(
        api_id: int,
        api_hash: str,
        bot_token: str,
        plugins: dict = None,
        cache_time: int = CACHE_TIME,
        session_name: str = SESSION_NAME,
) -> Bot:

    bot = Bot(
        name=session_name,
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token
    )

    @bot.on_message(filters=filters.command('start') & filters.private)
    async def hello(client: Client, message: Message) -> None:
        await message.reply(
            'Send me `Sticker` to get `FILE_ID`'
            '\nor\n'
            'Use `Inline Mode` to generate `Sticker`',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('Inline Mode', switch_inline_query='')]]
            )
        )

    @bot.on_message(filters=filters.private & filters.sticker)
    async def sticker(client: Client, message: Message) -> None:
        await message.reply(
            '**[FILE_ID]**\n'
            f'`{message.sticker.file_id}`',
            reply_to_message_id=message.id
        )

    async def handle_inline_query(bot: Bot, query: InlineQuery, iter_results):
        result = [i async for i in iter_results(bot, query)]
        await query.answer(
            result if any(result) else [
                InlineQueryResultArticle(
                    'No Sticker',
                    input_message_content=InputTextMessageContent(f'**Invalid Input:**\n`{query.query}`')
                )
            ],
            is_gallery=True,
            cache_time=cache_time,
        )

    def _async_partial(func, *args, **kwargs):
        async def async_func(*args2, **kwargs2):
            result = func(*args, *args2, **kwargs, **kwargs2)
            if asyncio.iscoroutinefunction(func):
                result = await result
            return result
        return async_func

    loader = pluginlib.PluginLoader(library=plugins['root'])
    inline_query: dict = loader.plugins.inline_query
    for name, cls in inline_query.items():
        logging.info(f'Loading Inline Query Plugin: {name}')
        plugin = cls()
        bot.add_handler(
            InlineQueryHandler(
                _async_partial(handle_inline_query, iter_results=plugin.iter_inline_query_results),
                filters.regex(plugin.inline_pattern)
            )
        )

    async def handle_command(bot: Bot, message: Message, reply_msg):
        await reply_msg(bot, message)

    command: dict = loader.plugins.command
    for name, cls in command.items():
        logging.info(f'Loading Command Plugin: {name}')
        plugin = cls()
        bot.add_handler(
            MessageHandler(
                _async_partial(handle_command, reply_msg=plugin.reply_msg),
                filters.private & filters.command(plugin.command)
            )
        )

    return bot
