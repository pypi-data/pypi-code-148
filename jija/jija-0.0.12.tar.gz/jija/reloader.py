import asyncio
import aiofile

import hashlib
import os


class Reloader:
    def __init__(self, root_path, event: asyncio.Event):
        self.__root_path = root_path
        self.__event = event
        self.__alive = True

    async def wait(self):
        last_hash = None
        while self.__alive:
            try:
                new_hash = await self.__get_hash(self.__root_path)
                if last_hash is None:
                    last_hash = new_hash

                if last_hash != new_hash and not self.__event.is_set():
                    last_hash = new_hash
                    self.__event.set()
                    await asyncio.sleep(3)

                await asyncio.sleep(1)

            except Exception as exception:
                print('Reloader caught an exception but still work')
                print(exception)
                print()
                await asyncio.sleep(5)

    async def __get_hash(self, path, pre_hash=None):
        if not pre_hash:
            pre_hash = hashlib.sha1()

        files = os.listdir(path)

        for file in files:
            next_path = f'{path}/{file}'
            if os.path.isdir(next_path):
                pre_hash = await self.__get_hash(next_path, pre_hash)

            else:
                async with aiofile.async_open(next_path, 'rb') as buffer:
                    chunk = 0
                    while chunk != b'':
                        chunk = await buffer.read(1024)
                        pre_hash.update(chunk)

        if path == self.__root_path:
            return pre_hash.hexdigest()

        return pre_hash

    def close(self):
        self.__alive = False
