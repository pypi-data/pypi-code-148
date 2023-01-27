import threading
import requests
import queue
import time
import asyncio
import logging

import eventlet


class RequestsDownloadingMixin(object):
    def download(self, *args, **kwargs):
        self.raw_output_data = requests.get(self.input_data)
        return self.raw_output_data


class SafePerformMixin(object):
    def actions_on_exceptions(self, exception, *args, **kwargs):
        raise NotImplementedError

    def perform(self, *args, **kwargs):
        try:
            super().perform(*args, **kwargs)
        except Exception as ex:
            self.actions_on_exceptions(ex, *args, **kwargs)


class MaxRepeatException(Exception):
    pass


class RepeatRecursivelyOnExceptionMixin(object):
    countdown_on_exception = 1
    max_repeats_on_exception = None  # None for no limit

    def actions_on_exceptions(self, exception, *args, **kwargs):
        attempt = getattr(self, "attempt", 0)
        time.sleep(self.countdown_on_exception)
        max_repeats = self.max_repeats_on_exception

        if max_repeats is not None and attempt <= max_repeats:
            attempt += 1
            self.__class__.perform(input_data=self.input_data, attempt=attempt,
                                   *self.input_args, **self.input_kwargs)
        else:
            raise MaxRepeatException()


class MultiThreadPerformMixin(object):
    perform_in_new_thread = True

    def __init__(self, *args, **kwargs):
        if kwargs.get("tasks", None) is None:
            # print("tasks is None")
            kwargs["tasks"] = queue.Queue()
        kwargs["tasks"].closed = False
        return super().__init__(*args, **kwargs)

    def wait_for_complete(self):
        self.tasks.join()
        self.actions_on_complete()

    def stop_all_uncompleted_tasks(self):
        try:
            self.tasks.closed = True

            for task in self.get_uncompleted_tasks():
                task._tstate_lock.release()
                task._stop()
        except Exception as ex:
            logging.error(
                f"An error has ocured on stop_all_uncompleted_tasks: {ex}")

    def actions_on_complete(self):
        pass

    def check_for_complete(self):
        return any([task.is_alive for task in self.tasks])

    def get_uncompleted_tasks(self):
        if self.tasks:
            return [task for task in self.tasks if task.is_alive]
        return []

    def perform_next_step(self, next_step_class, *args, **kwargs):
        kwargs["next_step_class"] = next_step_class

        # before_time = time.time()
        if not self.tasks.closed and next_step_class is not None:
            if next_step_class.perform_in_new_thread:

                is_daemon = getattr(self, "is_daemon", False)
                worker = threading.Thread(target=super().perform_next_step,
                                          args=args, kwargs=kwargs)
                worker.setDaemon(is_daemon)
                # self.tasks.put(worker)
                self.tasks.put(self)
                worker.start()
            else:
                self.tasks.put(self)
                super().perform_next_step(*args, **kwargs)

    def perform(self, *args, **kwargs):
        is_first_task = self.tasks.empty()
        super().perform(*args, **kwargs)
        if not is_first_task:
            # because first task in current thread
            self.tasks.task_done()


class AsyncMixin:
    async def async_get_next_step_class(self, *args, **kwargs):
        # return self.next_step_class
        return await asyncio.to_thread(
            self.get_next_step_class, *args, **kwargs
        )

    async def async_prepare_input_data(self, *args, **kwargs):
        return await asyncio.to_thread(
            self.prepare_input_data, *args, **kwargs
        )

    async def async_input_data_is_valid(self, *args, **kwargs):
        return await asyncio.to_thread(
            self.input_data_is_valid, *args, **kwargs
        )

    async def async_download(self, *args, **kwargs):
        return await asyncio.to_thread(
            self.download, *args, **kwargs
        )

    async def async_process_raw_data(self, *args, **kwargs):
        return await asyncio.to_thread(
            self.process_raw_data, *args, **kwargs
        )

    async def async_input_data_to_output_data(self, *args, **kwargs):
        return await asyncio.to_thread(
            self.input_data_to_output_data, *args, **kwargs
        )

    async def async_process_if_not_valid(self, *args, **kwargs):
        return await asyncio.to_thread(
            self.process_if_not_valid, *args, **kwargs
        )

    async def async_perform_next_step(self, *args, **kwargs):
        return self.perform_next_step(*args, **kwargs)

    async def async_save_data(self, *args, **kwargs):
        return self.save_data(*args, **kwargs)

    async def async_parse(self, *args, **kwargs):
        return self.parse(*args, **kwargs)

    async def async_perform(self, *args, **kwargs):
        return self.perform(*args, **kwargs)


class EventletPerformMixin(object):
    perform_in_new_thread = True

    def __init__(self, *args, **kwargs):
        if kwargs.get("tasks", None) is None:
            kwargs["tasks"] = eventlet.GreenPool(size=1000)
        return super().__init__(*args, **kwargs)

    def wait_for_complete(self):
        self.tasks.waitall()
        self.actions_on_complete()

    def stop_all_uncompleted_tasks(self):
        raise NotImplementedError

    def actions_on_complete(self):
        pass

    def check_for_complete(self):
        return not bool(self.tasks.running())

    def get_uncompleted_tasks(self):
        return self.tasks.coroutines_running

    def perform_next_step(self, next_step_class, *args, **kwargs):
        kwargs["next_step_class"] = next_step_class

        # before_time = time.time()
        if next_step_class is not None:
            self.tasks.spawn_n(super().perform_next_step, *args, **kwargs)
