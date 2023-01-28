from pathlib import Path

import httpx

from nonebot_plugin_baidutranslate.model import Translate
import asyncio

appid: str = "20220403001156610"
salt: str = "52Number_Sir"
key: str = "Vl5EC0q5kxupoJr5GkPD"

async def main():
    async with httpx.AsyncClient() as client:
        tr = Translate(client, appid, salt, key)
        # result = await Translate(client, appid, salt, key).field_translate(q="边际效用递减", from_="zh", to="en", domain="finance")
        # result = await tr.language_recognize(q="Je t'aime.")
        # result = await tr.document_count(file=Path("test.txt").absolute(), from_="zh", to="en", type_="txt")
        # result = await tr.document_translate(file=Path("test.txt").absolute(), from_="zh", to="en", type_="txt", output_type="txt")
        # result = await tr.picture_translate(image=Path("test.png").absolute(), from_="zh", to="en")
        # result = await tr.voice_translate(voice=Path("test.png").absolute(), from_="zh", to="en")
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
