# -*- coding: utf-8 -*-
from __future__ import print_function

from sent import util, types, apihelper

import threading
import time
import re
import sys
import six


class Telegram:
    def __init__(self, token, threaded=True, skip_pending=False):
        self.token = token
        self.update_listener = []
        self.skip_pending = skip_pending

        self.__stop_polling = threading.Event()
        self.last_update_id = 0
        self.exc_info = None

        self.message_subscribers_messages = []
        self.message_subscribers_callbacks = []
        self.message_subscribers_lock = threading.Lock()

        # key: chat_id, value: handler list
        self.message_subscribers_next_step = {}
        self.pre_message_subscribers_next_step = {}

        self.message_handlers = []
        self.inline_handlers = []
        self.chosen_inline_handlers = []
        self.callback_query_handlers = []

        self.threaded = threaded
        if self.threaded:
            self.worker_pool = util.ThreadPool()

    def set_webhook(self, url=None, certificate=None):
        return apihelper.set_webhook(self.token, url, certificate)

    def remove_webhook(self):
        return self.set_webhook()  # No params resets webhook

    def get_updates(self, offset=None, limit=None, timeout=20):
        json_updates = apihelper.get_updates(
            self.token, offset, limit, timeout)
        ret = []
        for ju in json_updates:
            ret.append(types.Update.de_json(ju))
        return ret

    def __skip_updates(self):
        total = 0
        updates = self.get_updates(offset=self.last_update_id, timeout=1)
        while updates:
            total += len(updates)
            for update in updates:
                if update.update_id > self.last_update_id:
                    self.last_update_id = update.update_id
            updates = self.get_updates(
                offset=self.last_update_id + 1, timeout=1)
        return total

    def __retrieve_updates(self, timeout=20):
        if self.skip_pending:
            self.skip_pending = False
        updates = self.get_updates(
            offset=(self.last_update_id + 1), timeout=timeout)
        self.process_new_updates(updates)

    def process_new_updates(self, updates):
        new_messages = []
        new_inline_querys = []
        new_chosen_inline_results = []
        new_callback_querys = []
        for update in updates:
            if update.update_id > self.last_update_id:
                self.last_update_id = update.update_id
            if update.message:
                new_messages.append(update.message)
            if update.inline_query:
                new_inline_querys.append(update.inline_query)
            if update.chosen_inline_result:
                new_chosen_inline_results.append(update.chosen_inline_result)
            if update.callback_query:
                new_callback_querys.append(update.callback_query)
        if len(new_messages) > 0:
            self.process_new_messages(new_messages)
        if len(new_inline_querys) > 0:
            self.process_new_inline_query(new_inline_querys)
        if len(new_chosen_inline_results) > 0:
            self.process_new_chosen_inline_query(new_chosen_inline_results)
        if len(new_callback_querys) > 0:
            self.process_new_callback_query(new_callback_querys)

    def process_new_messages(self, new_messages):
        self._append_pre_next_step_handler()
        self.__notify_update(new_messages)
        self._notify_command_handlers(self.message_handlers, new_messages)
        self._notify_message_subscribers(new_messages)
        self._notify_message_next_handler(new_messages)

    def process_new_inline_query(self, new_inline_querys):
        self._notify_command_handlers(self.inline_handlers, new_inline_querys)

    def process_new_chosen_inline_query(self, new_chosen_inline_querys):
        self._notify_command_handlers(
            self.chosen_inline_handlers, new_chosen_inline_querys)

    def process_new_callback_query(self, new_callback_querys):
        self._notify_command_handlers(
            self.callback_query_handlers, new_callback_querys)

    def __notify_update(self, new_messages):
        for listener in self.update_listener:
            self.__exec_task(listener, new_messages)

    def polling(self, none_stop=False, interval=0, timeout=20):
        if self.threaded:
            self.__threaded_polling(none_stop, interval, timeout)
        else:
            self.__non_threaded_polling(none_stop, interval, timeout)

    def __threaded_polling(self, none_stop=False, interval=0, timeout=3):
        self.__stop_polling.clear()
        error_interval = .25

        polling_thread = util.WorkerThread(name="PollingThread")
        or_event = util.OrEvent(
            polling_thread.done_event,
            polling_thread.exception_event,
            self.worker_pool.exception_event
        )

        while not self.__stop_polling.wait(interval):
            or_event.clear()
            try:
                polling_thread.put(self.__retrieve_updates, timeout)

                or_event.wait()  # wait for polling thread finish, polling thread error or thread pool error

                polling_thread.raise_exceptions()
                self.worker_pool.raise_exceptions()

                error_interval = .25
            except apihelper.ApiException as e:
                if not none_stop:
                    self.__stop_polling.set()
                else:
                    polling_thread.clear_exceptions()
                    self.worker_pool.clear_exceptions()
                    time.sleep(error_interval)
                    error_interval *= 2
            except KeyboardInterrupt:
                self.__stop_polling.set()
                polling_thread.stop()
                break

    def __non_threaded_polling(self, none_stop=False, interval=0, timeout=3):
        self.__stop_polling.clear()
        error_interval = .25

        while not self.__stop_polling.wait(interval):
            try:
                self.__retrieve_updates(timeout)
                error_interval = .25
            except apihelper.ApiException as e:
                if not none_stop:
                    self.__stop_polling.set()
                else:
                    time.sleep(error_interval)
                    error_interval *= 2
            except KeyboardInterrupt:
                self.__stop_polling.set()
                break

    def __exec_task(self, task, *args, **kwargs):
        if self.threaded:
            self.worker_pool.put(task, *args, **kwargs)
        else:
            task(*args, **kwargs)

    def stop_polling(self):
        self.__stop_polling.set()

    def set_update_listener(self, listener):
        self.update_listener.append(listener)

    def get_me(self):
        result = apihelper.get_me(self.token)
        return types.User.de_json(result)

    def get_file(self, file_id):
        return types.File.de_json(apihelper.get_file(self.token, file_id))

    def download_file(self, file_path):
        return apihelper.download_file(self.token, file_path)

    def get_user_profile_photos(self, user_id, offset=None, limit=None):
        result = apihelper.get_user_profile_photos(
            self.token, user_id, offset, limit)
        return types.UserProfilePhotos.de_json(result)

    def send_message(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                     parse_mode=None, disable_notification=None):
        return types.Message.de_json(
            apihelper.send_message(self.token, chat_id, text, disable_web_page_preview, reply_to_message_id,
                                   reply_markup, parse_mode, disable_notification))

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None):
        return types.Message.de_json(
            apihelper.forward_message(self.token, chat_id, from_chat_id, message_id, disable_notification))

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None,
                   disable_notification=None):
        return types.Message.de_json(
            apihelper.send_photo(self.token, chat_id, photo, caption, reply_to_message_id, reply_markup,
                                 disable_notification))

    def send_audio(self, chat_id, audio, duration=None, performer=None, title=None, reply_to_message_id=None,
                   reply_markup=None, disable_notification=None):
        return types.Message.de_json(
            apihelper.send_audio(self.token, chat_id, audio, duration, performer, title, reply_to_message_id,
                                 reply_markup, disable_notification))

    def send_voice(self, chat_id, voice, duration=None, reply_to_message_id=None, reply_markup=None,
                   disable_notification=None):
        return types.Message.de_json(
            apihelper.send_voice(self.token, chat_id, voice, duration, reply_to_message_id, reply_markup,
                                 disable_notification))

    def send_document(self, chat_id, data, reply_to_message_id=None, reply_markup=None, disable_notification=None):
        return types.Message.de_json(
            apihelper.send_data(self.token, chat_id, data, 'document', reply_to_message_id, reply_markup,
                                disable_notification))

    def send_sticker(self, chat_id, data, reply_to_message_id=None, reply_markup=None, disable_notification=None):
        return types.Message.de_json(
            apihelper.send_data(self.token, chat_id, data, 'sticker', reply_to_message_id, reply_markup,
                                disable_notification))

    def send_video(self, chat_id, data, duration=None, caption=None, reply_to_message_id=None, reply_markup=None,
                   disable_notification=None):
        return types.Message.de_json(
            apihelper.send_video(self.token, chat_id, data, duration, caption, reply_to_message_id, reply_markup,
                                 disable_notification))

    def send_location(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None,
                      disable_notification=None):
        return types.Message.de_json(
            apihelper.send_location(self.token, chat_id, latitude, longitude, reply_to_message_id, reply_markup,
                                    disable_notification))

    def send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, disable_notification=None,
                   reply_to_message_id=None, reply_markup=None):
        return types.Message.de_json(
            apihelper.send_venue(self.token, chat_id, latitude, longitude, title, address, foursquare_id,
                                 disable_notification, reply_to_message_id, reply_markup)
        )

    def send_contact(self, chat_id, phone_number, first_name, last_name=None, disable_notification=None,
                     reply_to_message_id=None, reply_markup=None):
        return types.Message.de_json(
            apihelper.send_contact(self.token, chat_id, phone_number, first_name, last_name, disable_notification,
                                   reply_to_message_id, reply_markup)
        )

    def send_chat_action(self, chat_id, action):
        return apihelper.send_chat_action(self.token, chat_id, action)

    def kick_chat_member(self, chat_id, user_id):
        return apihelper.kick_chat_member(self.token, chat_id, user_id)

    def unban_chat_member(self, chat_id, user_id):
        return apihelper.unban_chat_member(self.token, chat_id, user_id)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=None):
        return apihelper.answer_callback_query(self.token, callback_query_id, text, show_alert)

    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                          disable_web_page_preview=None, reply_markup=None):
        result = apihelper.edit_message_text(self.token, text, chat_id, message_id, inline_message_id, parse_mode,
                                             disable_web_page_preview, reply_markup)
        # if edit inline message return is bool not Message.
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def edit_message_replay_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return types.Message.de_json(
            apihelper.edit_message_replay_markup(
                self.token, chat_id, message_id, inline_message_id, reply_markup)
        )

    def edit_message_caption(self, caption, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return types.Message.de_json(
            apihelper.edit_message_caption(
                self.token, caption, chat_id, message_id, inline_message_id, reply_markup)
        )

    def reply_to(self, message, text, **kwargs):
        return self.send_message(message.chat.id, text, reply_to_message_id=message.message_id, **kwargs)

    def answer_inline_query(self, inline_query_id, results, cache_time=None, is_personal=None, next_offset=None,
                            switch_pm_text=None, switch_pm_parameter=None):
        return apihelper.answer_inline_query(self.token, inline_query_id, results, cache_time, is_personal, next_offset,
                                             switch_pm_text, switch_pm_parameter)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=None):
        return apihelper.answer_callback_query(self.token, callback_query_id, text, show_alert)

    def register_for_reply(self, message, callback):
        with self.message_subscribers_lock:
            self.message_subscribers_messages.insert(0, message.message_id)
            self.message_subscribers_callbacks.insert(0, callback)
            if len(self.message_subscribers_messages) > 10000:
                self.message_subscribers_messages.pop()
                self.message_subscribers_callbacks.pop()

    def _notify_message_subscribers(self, new_messages):
        for message in new_messages:
            if not message.reply_to_message:
                continue

            reply_msg_id = message.reply_to_message.message_id
            if reply_msg_id in self.message_subscribers_messages:
                index = self.message_subscribers_messages.index(reply_msg_id)
                self.message_subscribers_callbacks[index](message)

                with self.message_subscribers_lock:
                    index = self.message_subscribers_messages.index(
                        reply_msg_id)
                    del self.message_subscribers_messages[index]
                    del self.message_subscribers_callbacks[index]

    def register_next_step_handler(self, message, callback):
        chat_id = message.chat.id
        if chat_id in self.pre_message_subscribers_next_step:
            self.pre_message_subscribers_next_step[chat_id].append(callback)
        else:
            self.pre_message_subscribers_next_step[chat_id] = [callback]

    def _notify_message_next_handler(self, new_messages):
        for message in new_messages:
            chat_id = message.chat.id
            if chat_id in self.message_subscribers_next_step:
                handlers = self.message_subscribers_next_step[chat_id]
                for handler in handlers:
                    self.__exec_task(handler, message)
                self.message_subscribers_next_step.pop(chat_id, None)

    def _append_pre_next_step_handler(self):
        for k in self.pre_message_subscribers_next_step.keys():
            if k in self.message_subscribers_next_step:
                self.message_subscribers_next_step[k].extend(
                    self.pre_message_subscribers_next_step[k])
            else:
                self.message_subscribers_next_step[k] = self.pre_message_subscribers_next_step[k]
        self.pre_message_subscribers_next_step = {}

    def message_handler(self, commands=None, regexp=None, func=None, content_types=['text']):
        def decorator(handler):
            self.add_message_handler(
                handler, commands, regexp, func, content_types)
            return handler

        return decorator

    def add_message_handler(self, handler, commands=None, regexp=None, func=None, content_types=None):
        if content_types is None:
            content_types = ['text']

        filters = {'content_types': content_types}
        if regexp:
            filters['regexp'] = regexp
        if func:
            filters['lambda'] = func
        if commands:
            filters['commands'] = commands

        handler_dict = {
            'function': handler,
            'filters': filters
        }

        self.message_handlers.append(handler_dict)

    def inline_handler(self, func):
        def decorator(handler):
            self.add_inline_handler(handler, func)
            return handler

        return decorator

    def add_inline_handler(self, handler, func):
        filters = {'lambda': func}

        handler_dict = {
            'function': handler,
            'filters': filters
        }

        self.inline_handlers.append(handler_dict)

    def chosen_inline_handler(self, func):
        def decorator(handler):
            self.add_chosen_inline_handler(handler, func)
            return handler

        return decorator

    def add_chosen_inline_handler(self, handler, func):
        filters = {'lambda': func}

        handler_dict = {
            'function': handler,
            'filters': filters
        }

        self.chosen_inline_handlers.append(handler_dict)

    def callback_query_handler(self, func):
        def decorator(handler):
            self.add_callback_query_handler(handler, func)

        return decorator

    def add_callback_query_handler(self, handler, func):
        filters = {'lambda': func}

        handler_dict = {
            'function': handler,
            'filters': filters
        }

        self.callback_query_handlers.append(handler_dict)

    @staticmethod
    def _test_message_handler(message_handler, message):
        for filter, filter_value in six.iteritems(message_handler['filters']):
            if not Telegram._test_filter(filter, filter_value, message):
                return False
        return True

    @staticmethod
    def _test_filter(filter, filter_value, message):
        if filter == 'content_types':
            return message.content_type in filter_value
        if filter == 'regexp':
            return message.content_type == 'text' and re.search(filter_value, message.text)
        if filter == 'commands':
            return message.content_type == 'text' and util.extract_command(message.text) in filter_value
        if filter == 'lambda':
            return filter_value(message)
        return False

    def _notify_command_handlers(self, handlers, new_messages):
        for message in new_messages:
            for message_handler in handlers:
                if self._test_message_handler(message_handler, message):
                    self.__exec_task(message_handler['function'], message)
                    break


class AsyncTelegram(Telegram):
    def __init__(self, *args, **kwargs):
        Telegram.__init__(self, *args, **kwargs)

    @util.asyncd()
    def get_me(self):
        return Telegram.get_me(self)

    @util.asyncd()
    def get_user_profile_photos(self, *args, **kwargs):
        return Telegram.get_user_profile_photos(self, *args, **kwargs)

    @util.asyncd()
    def send_message(self, *args, **kwargs):
        return Telegram.send_message(self, *args, **kwargs)

    @util.asyncd()
    def forward_message(self, *args, **kwargs):
        return Telegram.forward_message(self, *args, **kwargs)

    @util.asyncd()
    def send_photo(self, *args, **kwargs):
        return Telegram.send_photo(self, *args, **kwargs)

    @util.asyncd()
    def send_audio(self, *args, **kwargs):
        return Telegram.send_audio(self, *args, **kwargs)

    @util.asyncd()
    def send_document(self, *args, **kwargs):
        return Telegram.send_document(self, *args, **kwargs)

    @util.asyncd()
    def send_sticker(self, *args, **kwargs):
        return Telegram.send_sticker(self, *args, **kwargs)

    @util.asyncd()
    def send_video(self, *args, **kwargs):
        return Telegram.send_video(self, *args, **kwargs)

    @util.asyncd()
    def send_location(self, *args, **kwargs):
        return Telegram.send_location(self, *args, **kwargs)

    @util.asyncd()
    def send_chat_action(self, *args, **kwargs):
        return Telegram.send_chat_action(self, *args, **kwargs)
