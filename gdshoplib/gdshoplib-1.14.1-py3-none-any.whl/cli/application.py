import time
from multiprocessing import Pool
from typing import Optional

import typer
from rich import print

from gdshoplib import Platform, Product
from gdshoplib.apps.finance.storage import Storage
from gdshoplib.packages.cache import KeyDBCache
from gdshoplib.packages.feed import Feed
from gdshoplib.packages.s3 import S3, SimpleS3Data
from gdshoplib.services.notion.database import Database
from gdshoplib.services.notion.notion import Notion
from gdshoplib.services.vk.market import VKMarket
from gdshoplib.services.vk.vk import VK

app = typer.Typer()


@app.command()
def sku_set():
    for page in Product.query(
        params={
            "filter": {
                "and": [
                    {"property": "Наш SKU", "rich_text": {"is_empty": True}},
                    {"property": "Цена (eur)", "number": {"is_not_empty": True}},
                ]
            }
        },
    ):
        sku = page.generate_sku()
        while not Product.query(filter={"sku": sku}):
            sku = page.generate_sku()

        page.notion.update_prop(
            page.id, params={"properties": {"Наш SKU": [{"text": {"content": sku}}]}}
        )
        print(Product(page.id).sku)


def price_update_action(id):
    product = Product(id)
    props_map = {
        "price_now": dict(name="Текущая Цена", value=product.price.now),
        "price_kit": dict(name="Цена комплекта", value=product.price.get_kit_price()),
        "price_neitral": dict(name="Безубыточность", value=product.price.neitral),
        "price_current_discount": dict(
            name="Текущая Скидка", value=product.price.current_discount
        ),
        "price_agent": dict(name="Агентская Цена", value=product.price.neitral),
        "price_agent_kit": dict(
            name="Агентский комплект",
            value=product.price.get_kit_price(base_price="neitral"),
        ),
        "price_gross": dict(name="Себестоимость", value=product.price.gross),
    }

    for k, v in props_map.items():
        if not product[k] and not v["value"] or product[k] == v["value"]:
            continue

        product.notion.update_prop(
            product.id, params={"properties": {v["name"]: {"number": v["value"]}}}
        )
        print(f'{product.sku}: {v["name"]} ({v["value"]})')


@app.command()
def price_update(
    sku: Optional[str] = typer.Option(None),
    single: bool = typer.Option(False),
    loop_iteration: Optional[int] = typer.Option(None),
):
    while True:
        if sku:
            price_update_action(Product.get(sku).id)
            return

        if single:
            for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                price_update_action(product["id"])
        else:
            with Pool(3) as p:
                for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                    p.apply_async(price_update_action, (product["id"],))
                p.close()
                p.join()

        if loop_iteration:
            time.sleep(loop_iteration)
        else:
            break


def generate_description(id):
    product = Product(id)
    product.description.warm_description_blocks()
    for platform, block in product.description.description_blocks.items():
        key = platform.split(":")[-1]
        platform = Platform.get_platform(key=key)
        new_description = product.description.generate(platform.manager)
        Notion().update_block(
            block.id,
            params={"code": {"rich_text": [{"text": {"content": new_description}}]}},
        )
        print(f"{product.sku}: {platform}")


@app.command()
def description_regenerate(single: bool = typer.Option(False)):
    if single:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            generate_description(product["id"])
    else:
        with Pool(3) as p:
            for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                p.apply_async(generate_description, (product["id"],))
            p.close()
            p.join()


def description_check_action(id):
    product = Product(id)
    for platform_manager in Platform.__subclasses__():
        block = product.description.get_description_block(
            platform_key=platform_manager.KEY
        )
        print(f'{product.sku} {platform_manager}: {block.check if block else "None"}')


@app.command()
def description_check(single: bool = typer.Option(False)):
    with Pool(3) as p:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            p.apply_async(description_check_action, (product["id"],))
        p.close()
        p.join()


@app.command()
def cache_clean(id: Optional[str] = typer.Option(None)):
    # TODO: сделать удаление по ID
    KeyDBCache().clean(r"[blocks|pages|databases]*")


def cache_warm_func(id):
    product = Product(id)
    product.price.now
    product.kit
    product.notes
    product.specifications
    product.tags
    product.media
    product.description
    product.brand.title
    product.description.warm_description_blocks()
    print(f"{product.sku}: {product.last_edited_time}")


@app.command()
def cache_warm(
    only_exists: bool = typer.Option(False),
    single: bool = typer.Option(False),
    only_edited: bool = typer.Option(True),
    sku: Optional[str] = typer.Option(None),
    loop_iteration: Optional[int] = typer.Option(None),
):
    while True:
        if sku:
            cache_warm_func(Product.get(sku).id)
            return

        if single:
            with Database(
                Product.SETTINGS.PRODUCT_DB, notion=Notion(caching=True)
            ) as database:
                params = {}
                if only_edited and database.get_update_time():
                    print(f"Фильтрация от даты: {database.get_update_time()}")
                    params = database.edited_filter()

                for product in database.pages(params=params):
                    skipped = False
                    if only_exists:
                        if KeyDBCache().exists(product["id"]):
                            print(f"{product['id']}: SKIPPED")
                            skipped = True

                    if not skipped:
                        cache_warm_func(product["id"])
        else:
            with Pool(3) as p:
                with Database(
                    Product.SETTINGS.PRODUCT_DB, notion=Notion(caching=True)
                ) as database:
                    params = {}
                    if only_edited and database.get_update_time():
                        print(f"Фильтрация от даты: {database.get_update_time()}")
                        params = database.edited_filter()

                    for product in database.pages(params=params):
                        skipped = False
                        if only_exists:
                            if KeyDBCache().exists(product["id"]):
                                print(f"{product['id']}: SKIPPED")
                                skipped = True

                        if not skipped:
                            p.apply_async(cache_warm_func, (product["id"],))
                p.close()
                p.join()

        if loop_iteration:
            print("-" * 20)
            time.sleep(loop_iteration)
        else:
            break


@app.command()
def cache_count():
    print(KeyDBCache().count())


def cache_check_action(id):
    for block in Notion().get_blocks(id):
        exists = KeyDBCache().exists(block["id"])
        print(f"{block['id']}: {exists}")


@app.command()
def cache_check(single: bool = typer.Option(False)):
    if single:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            cache_check_action(product["id"])
    else:
        with Pool(3) as p:
            for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                p.apply_async(cache_check_action, (product["id"],))
            p.close()
            p.join()


def warm_product_media(id, with_badges):
    for media in Product(id).media:
        media.fetch()
        print(f"{media.s3}: {media.exists()}")
        if with_badges and media.badges:
            render = media.apply_badges()
            badged = S3(
                SimpleS3Data(
                    render.content,
                    None,
                    render.info["mime"],
                    file_info={
                        "id": media.id,
                        "format": render.info["format"],
                        "prefix": "BADGED",
                    },
                    parent=media.parent,
                )
            )
            badged.put()
            print(f"{badged} {badged.exists()}")


@app.command()
def media_warm(
    single: bool = typer.Option(False),
    with_badges: bool = typer.Option(False),
    loop_iteration: Optional[int] = typer.Option(None),
):
    while True:
        if single:
            for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                warm_product_media(product["id"], with_badges)
        else:
            with Pool(7) as p:
                for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                    p.apply_async(warm_product_media, (product["id"], with_badges))
                p.close()
                p.join()

        if loop_iteration:
            time.sleep(loop_iteration)
        else:
            break


@app.command()
def media_clean():
    s3 = S3(SimpleS3Data(None, file_key=None))
    s3.clean(pattern="Contents[? !contains(Key, `feed.`)][]")


@app.command()
def media_search(file_key=None):
    s3 = S3(SimpleS3Data(None, file_key=None))
    for object in s3.search(pattern=file_key):
        print(object)


@app.command()
def media_count():
    count = 0
    for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
        count += len(Product(product["id"]).media)

    print(count)


def media_check_action(id):
    accepted_formats = (
        "png",
        "jpg",
        "jpeg",
    )
    product = Product(id)
    for media in Product(product.id).media:
        accepted = media.format in accepted_formats
        print(
            f"{media.file_key}: {media.exists()} {'ACCEPTED' if accepted else 'REJECTED'}"
        )


@app.command()
def media_check(single: bool = typer.Option(False)):
    if single:
        for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
            media_check_action(product["id"])
    else:
        with Pool(3) as p:
            for product in Database(Product.SETTINGS.PRODUCT_DB).pages():
                p.apply_async(media_check_action, (product["id"],))
            p.close()
            p.join()


def warm_platfrom_feed(key):
    platform = Feed.get_platform_class(key=key)
    platform().push_feed()
    print(platform)


@app.command()
def feed_warm(platform_key=None, loop_iteration: Optional[int] = typer.Option(None)):
    while True:
        if platform_key:
            warm_platfrom_feed(platform_key)
            return

        for platform in [Feed, *[feed for feed in Feed.__subclasses__()]]:
            warm_platfrom_feed(platform.KEY)

        if loop_iteration:
            time.sleep(loop_iteration)
        else:
            break


@app.command()
def vk_get_access_code(code=None):
    if not code:
        VK().get_oauth_code()
        code = typer.prompt("Код")

    print(VK().get_access_token(code))


@app.command()
def vk_health():
    assert VKMarket().list(), "Запрос в VK не выполняется"
    print("OK")


@app.command()
def finance_storage_amount(base_price="now"):
    print(f"{base_price}: {Storage().amount(Product.query(), base_price=base_price)}")


if __name__ == "__main__":
    app()
