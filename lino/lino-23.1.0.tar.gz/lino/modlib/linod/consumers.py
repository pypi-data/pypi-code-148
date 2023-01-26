# -*- coding: UTF-8 -*-
# Copyright 2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import asyncio
import json
import os
import pickle
import schedule
import signal
import socket
import sys
from pathlib import Path

from django.conf import settings
from channels.db import database_sync_to_async


try:
    from pywebpush import webpush, WebPushException
except ImportError:
    webpush = None

from channels.consumer import AsyncConsumer

import logging
import struct

from lino.utils.socks import send_through_socket, get_from_socket, unlink

logger = logging.getLogger('linod')

class LogReceiver(asyncio.BufferedProtocol):
    # Tailored from: https://gist.github.com/1st1/1c606e5b83ef0e9c41faf21564d75ad7
    def connection_made(self, transport) -> None:
        self.transport = transport
        self._msg_size = None
        self._new_buffer(4)

    def _new_buffer(self, size):
        self.buffer = bytearray(size)
        self.pos = 0

    def get_buffer(self, sizehint: int) -> bytearray:
        return self.buffer

    def buffer_updated(self, nbytes: int) -> None:
        self.pos += nbytes

        if self._msg_size is None:
            if self.pos == 4:
                self._msg_size = struct.unpack('>L', self.buffer)[0]
                self._new_buffer(self._msg_size)
        else:
            if int(self.pos) == int(self._msg_size):
                msg = self.buffer
                self._new_buffer(4)
                self._msg_size = None

                self.message_received(msg)

    def message_received(self, data: bytes) -> None:
        data = pickle.loads(data)
        record = logging.makeLogRecord(data)
        logger.handle(record)
        self.transport.close()

class LinodConsumer(AsyncConsumer):

    deferred_jobs = []
    clients = set()
    pid = None
    log_sock = settings.SITE.site_dir / 'log_sock'
    worker_sock = settings.SITE.site_dir / 'worker_sock'

    def remove_socks(self):
        unlink(str(self.log_sock))
        unlink(str(self.worker_sock))

    def handle_signal(self, sig, frame):
        self.remove_socks()
        signal.raise_signal(sig)

    def register_signals(self):
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    async def log_server(self, event=None):
        logger.info("Running log server")
        asyncio.ensure_future(self.async_log_server())

    async def async_log_server(self):
        self.register_signals()
        loop = asyncio.get_running_loop()
        log_sock = self.get_log_sock()
        server = await loop.create_unix_server(lambda : LogReceiver(), log_sock)
        try:
            async with server:
                await server.serve_forever()
        finally:
            unlink(log_sock)

    def get_log_sock(self):
        log_sock = str(self.log_sock)
        unlink(log_sock)
        return log_sock

    async def unused_send_push(self, event):
        # logger.info("Push to %s : %s", user or "everyone", data)
        data = event['data']
        user = event['user_id']
        if user is not None:
            user = settings.SITE.models.users.User.objects.get(pk=user)
        kwargs = dict(
            data=json.dumps(data),
            vapid_private_key=settings.SITE.plugins.notify.vapid_private_key,
            vapid_claims={
                'sub': "mailto:{}".format(settings.SITE.plugins.notify.vapid_admin_email)
            }
        )
        if user is None:
            subs = settings.SITE.models.notify.Subscription.objects.all()
        else:
            subs = settings.SITE.models.notify.Subscription.objects.filter(user=user)
        for sub in subs:
            sub_info = {
                'endpoint': sub.endpoint,
                'keys': {
                    'p256dh': sub.p256dh,
                    'auth': sub.auth,
                },
            }
            try:
                req = webpush(subscription_info=sub_info, **kwargs)
            except WebPushException as e:
                if e.response.status_code == 410:
                    sub.delete()
                else:
                    raise e

    async def run_schedule(self, event):
        asyncio.ensure_future(self._run_schedule(event.get('run_all', False)))

    async def _run_schedule(self, run_all):
        """
        :param run_all: Runs all the jobs at once regardless of their schedule, use only for testing purposes.
        """
        logger.info("Running schedule")
        n = len(schedule.jobs)
        if n == 0:
            logger.info("This site has no scheduled jobs.")
            return
        logger.info(f"{n} scheduled jobs:")
        for i, job in enumerate(schedule.jobs, 1):
            logger.info(f"[{i}] {repr(job)}")
        if run_all:
            try:
                await database_sync_to_async(schedule.run_all)()
            except Exception as e:
                logger.exception(e)
        else:
            while True:
                await database_sync_to_async(schedule.run_pending)()
                await asyncio.sleep(1)

    async def dev_worker(self, event: dict):
        worker_sock = str(self.worker_sock)
        self.pid = event['pid']

        def add_client(sock: socket.socket) -> None:
            self.clients.add(get_from_socket(sock))
            sock.close()

        def remove_client(sock: socket.socket, close: bool = True) -> None:
            self.clients.discard(get_from_socket(sock))
            if close:
                sock.close()

        def client_exists(sock: socket.socket) -> None:
            if get_from_socket(sock) in self.clients:
                send_through_socket(sock, b'true')
            else:
                send_through_socket(sock, b'false')
            handle_msg(sock)

        def process_remove_get(sock: socket.socket) -> None:
            remove_client(sock, False)
            data = pickle.dumps({'clients': len(self.clients), 'pid': self.pid})
            send_through_socket(sock, data)
            sock.close()

        SIGNALS = {
            b'add': add_client,
            b'exists': client_exists,
            b'remove': remove_client,
            b'remove_get': process_remove_get,
            b'close': lambda sock: sock.close()
        }

        def handle_msg(client_sock: socket.socket) -> None:
            msg = get_from_socket(client_sock)
            if msg not in SIGNALS:
                senc_thourgh_socket(client_sock, b"Invalid signal!")
                client_sock.close()
            else:
                SIGNALS[msg](client_sock)

        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                unlink(worker_sock)
                sock.bind(worker_sock)
                sock.listen(5)
                while True:
                    client_sock, _ = sock.accept()
                    handle_msg(client_sock)
        finally:
            unlink(worker_sock)

    async def job_deferred_list(self, event):
        async def do():
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sockd = str(settings.SITE.site_dir / 'sockd')
                sock.connect(sockd)
                data = pickle.dumps(self.deferred_jobs)
                await asyncio.sleep(1)
                send_through_socket(sock, data)
        asyncio.ensure_future(do())

    async def deferred_job(self, event):
        name = event['name']
        if name not in self.deferred_jobs:
            self.deferred_jobs.append(name)
