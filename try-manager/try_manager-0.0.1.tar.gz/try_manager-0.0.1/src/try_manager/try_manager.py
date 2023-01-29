import time
# from config import TOKEN
from aiogram import Bot, Dispatcher, types
# from vpnme import bot

TOKEN="YOUR_TOKEN_HERE"

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML) 

class User_try_aiogram():
    
    async def try_delete_message(self, obj):
        '''send call or message object or message_id for delete message'''
        if isinstance(obj, types.CallbackQuery):
            message_id=obj.message.message_id
        elif isinstance(obj, types.Message):
            message_id=obj.message_id
        else:
            message_id=obj
        try:
            answer = await bot.delete_message(chat_id=self.id, message_id=message_id)
        except Exception as e:
            print(log_time(), f" error delete message to user {self.id}")
            if e.match=='bot was blocked by the user':
                # self.black_list()
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer

    async def try_reply(
            self, 
            obj:types.Message,
            text,
            parse_mode=None,
            entities = None,
            disable_web_page_preview = None,
            disable_notification=None,
            protect_content=None, 
            allow_sending_without_reply=None,
            reply_markup=None):
        if isinstance(obj, types.CallbackQuery):
            obj=obj.message
        try:
            answer = await obj.reply(
                                text=text,
                                parse_mode=parse_mode, 
                                entities=entities, 
                                disable_web_page_preview=disable_web_page_preview, 
                                disable_notification=disable_notification, 
                                protect_content=protect_content, 
                                allow_sending_without_reply=allow_sending_without_reply, 
                                reply_markup=reply_markup)
        except Exception as e:
            print(log_time(), f" error reply message to user {self.id}")
            if e.match=='bot was blocked by the user':
                # self.black_list()
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer
    
    async def try_answer(
                self,
                obj:types.Message, 
                text, 
                parse_mode=None, 
                entities=None, 
                disable_web_page_preview=None,
                disable_notification=None,
                protect_content= None,
                allow_sending_without_reply=None, 
                reply_markup=None):
        if isinstance(obj, types.CallbackQuery):
            obj=obj.message
        try:
            answer = await obj.answer(
                                text=text, 
                                parse_mode=parse_mode, 
                                entities=entities, 
                                disable_web_page_preview=disable_web_page_preview,
                                disable_notification=disable_notification,
                                protect_content=protect_content,
                                allow_sending_without_reply=allow_sending_without_reply, 
                                reply_markup=reply_markup)
        except Exception as e:
            print(log_time(), f" error answer message to user {self.id}")
            if e.match=='bot was blocked by the user':
                # self.black_list()
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer

    async def try_send_message(
                        self, 
                        text,
                        parse_mode=None,
                        entities=None,
                        disable_web_page_preview=None,
                        disable_notification=None,
                        protect_content=None,
                        reply_to_message_id=None,
                        allow_sending_without_reply=None,
                        reply_markup=None):
        try:
            answer = await bot.send_message(
                                    chat_id=self.id, 
                                    text=text, 
                                    parse_mode=parse_mode,
                                    entities=entities,
                                    disable_web_page_preview=disable_web_page_preview,
                                    disable_notification=disable_notification,
                                    protect_content=protect_content,
                                    reply_to_message_id=reply_to_message_id,
                                    allow_sending_without_reply=allow_sending_without_reply,
                                    reply_markup=reply_markup)
        except Exception as e:
            print(log_time(), f" error send message to user {self.id}")
            if e.match=='bot was blocked by the user':
                # self.black_list()
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer

    async def try_edit_message_text(
                        self, 
                        text,
                        message_id,
                        inline_message_id=None,
                        parse_mode=None,
                        entities=None,
                        disable_web_page_preview=None,
                        reply_markup=None):
        try:
            answer = await bot.edit_message_text(
                                    text=text, 
                                    chat_id=self.id,
                                    message_id=message_id, 
                                    inline_message_id=inline_message_id, 
                                    parse_mode=parse_mode,
                                    entities=entities,
                                    disable_web_page_preview=disable_web_page_preview,
                                    reply_markup=reply_markup)
        except Exception as e:
            print(log_time(), f" error edit message to user {self.id}")
            if e.match=='bot was blocked by the user':
                # self.black_list()
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer
    
    async def try_send_document(
                        self, 
                        document,
                        thumb=None,
                        caption=None,
                        parse_mode=None,
                        caption_entities=None,
                        disable_content_type_detection=None,
                        disable_notification=None,
                        protect_content=None,
                        reply_to_message_id=None,
                        allow_sending_without_reply=None,
                        reply_markup=None):
        try:
            answer = await bot.send_document(
                            chat_id=self.id, 
                            document=document,
                            thumb=thumb,
                            caption=caption,
                            parse_mode=parse_mode,
                            caption_entities=caption_entities,
                            disable_content_type_detection=disable_content_type_detection,
                            disable_notification=disable_notification,
                            protect_content=protect_content,
                            reply_to_message_id=reply_to_message_id,
                            allow_sending_without_reply=allow_sending_without_reply,
                            reply_markup=reply_markup)
        except Exception as e:
            print(log_time(), f" error send document to user {self.id}")
            if e.match=='bot was blocked by the user':
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer
    
    async def try_send_video(
                        self, 
                        video,
                        duration=None,
                        width=None,
                        height=None,
                        thumb=None,
                        caption=None,
                        parse_mode=None,
                        caption_entities=None,
                        supports_streaming=None,
                        disable_notification=None,
                        protect_content=None,
                        reply_to_message_id=None,
                        allow_sending_without_reply=None,
                        reply_markup=None):
        try:
            answer = await bot.send_video(
                            chat_id=self.id,
                            video=video,
                            duration=duration,
                            width=width,
                            height=height,
                            thumb=thumb,
                            caption=caption,
                            parse_mode=parse_mode,
                            caption_entities=caption_entities,
                            supports_streaming=supports_streaming,
                            disable_notification=disable_notification,
                            protect_content=protect_content,
                            reply_to_message_id=reply_to_message_id,
                            allow_sending_without_reply=allow_sending_without_reply,
                            reply_markup=reply_markup)
        except Exception as e:
            print(log_time(), f" error send video to user {self.id}")
            if e.match=='bot was blocked by the user':
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer
        
    async def try_call_answer(
                        self, 
                        obj:types.CallbackQuery, 
                        text=None, 
                        show_alert=False,
                        url=None, 
                        cache_time=None):
        try:
            answer = await obj.answer(
                        text=text,
                        show_alert=show_alert,
                        url=url,
                        cache_time=cache_time)
        except Exception as e:
            print(log_time(), f" error callback answer to user {self.id}")
            if e.match=='bot was blocked by the user':
                print(log_time(), f" user {self.id} add to black list")
            else:
                print(e)
        else:
            return answer
#____________________________________________Function____________________________________________
def log_time():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime('%d/%m/%Y, %H:%M:%S', named_tuple)
    return(time_string)