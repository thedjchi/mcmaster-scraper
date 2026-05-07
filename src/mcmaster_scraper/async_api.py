from asyncio import TaskGroup

import diskcache as dc
import hashlib

import platformdirs
from pandas import DataFrame, concat

from ._api.table_parser import get_product_tables
from ._api.scraper import get_product_api_response
from ._utils.event_loop_wrapper import run_in_loop_async


# TODO add example to doc https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
# TODO automate playwright install
# TODO complete packaging
# https://docs.astral.sh/uv/guides/package/
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://www.pyopensci.org/python-package-guide/

async def get_products_from_url(
        url: str,
        refresh: bool = False
) -> DataFrame:
    """ Gets product tables from a given McMaster-Carr URL.

        If there are multiple product tables, they will be merged, and an additional "Product Type" column will be added.

        Parameters
        ----------
        url : str
            The URL to scrape. Must be a valid McMaster-Carr URL. The product tables must be visible on the webpage.
        refresh : bool, optional
            Whether to refresh the cached data. Default is False.

        Returns
        -------
        DataFrame
            A pandas DataFrame containing the combined product tables.

        Raises
        ------
        ValueError
            If the URL is not a valid McMaster-Carr URL.
        """
    cache_dir = platformdirs.user_cache_dir("mcmaster-scraper", None)
    cache = dc.Cache(cache_dir, eviction_policy="least-recently-used")
    key = hashlib.md5(url.encode()).hexdigest()

    if key in cache and not refresh:
        json = cache[key]
    else:
        json = await run_in_loop_async(get_product_api_response(url))
        cache[key] = json

    tables = get_product_tables(json)
    tables_with_product_type = [table.assign(**{"Product Type": product}) for product, table in tables.items()]
    return concat(tables_with_product_type, ignore_index=True)


async def get_products_from_urls(urls: list[str], refresh: bool = False) -> list[DataFrame]:
    """ Gets product tables from a list of McMaster-Carr URLs.

        See Also
        --------
        get_products_from_url
        """
    async with TaskGroup() as tg:
        tasks = [tg.create_task(get_products_from_url(url, refresh)) for url in urls]

    return [task.result() for task in tasks]
