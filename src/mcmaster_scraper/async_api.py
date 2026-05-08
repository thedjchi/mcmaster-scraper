import hashlib
from asyncio import create_task, gather

import diskcache as dc
import platformdirs
from pandas import DataFrame, concat

from ._api.scraper import get_product_api_response
from ._api.table_parser import get_product_tables
from ._utils.event_loop_wrapper import run_in_loop_async


async def get_products_from_url(url: str, refresh: bool = False) -> DataFrame:
    """Gets product tables from a McMaster-Carr URL.

    See Also
    --------
    sync_api.get_products_from_url
    """
    cache_dir = platformdirs.user_cache_dir(
        appname="mcmaster-scraper", appauthor=False, ensure_exists=True
    )
    cache = dc.Cache(cache_dir, eviction_policy="least-recently-used")
    key = hashlib.md5(url.encode()).hexdigest()

    if key in cache and not refresh:
        json = cache[key]
    else:
        json = await run_in_loop_async(get_product_api_response(url))
        cache[key] = json

    tables = get_product_tables(json)
    tables_with_product_type = [
        table.assign(**{"Product Type": product}) for product, table in tables.items()
    ]
    return concat(tables_with_product_type, ignore_index=True)


async def get_products_from_urls(
    urls: list[str], refresh: bool = False
) -> list[DataFrame]:
    """Gets product tables from a list of McMaster-Carr URLs.

    See Also
    --------
    sync_api.get_products_from_urls
    """
    tasks = [create_task(get_products_from_url(url, refresh)) for url in urls]
    return await gather(*tasks)
