from aiohttp import web


@web.middleware
class Middleware:
    async def handler(self, request: web.Request, handler):
        raise NotImplementedError()

    async def __call__(self, request: web.Request, handler):
        return await self.handler(request, handler)
