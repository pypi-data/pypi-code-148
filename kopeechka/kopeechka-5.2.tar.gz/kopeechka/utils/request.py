import aiohttp

async def request_get(url: str, params: dict, type_kopeechka):
    async with aiohttp.ClientSession() as session:
        for key in {key:params[key] for key in params}:
            if not params.get(key):
                params.pop(key)
        async with session.get(url=url, params=params) as response:
            return type_kopeechka(await response.json())