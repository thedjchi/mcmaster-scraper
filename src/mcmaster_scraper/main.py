import diskcache as dc
import hashlib
from pandas import DataFrame

from .api.tableparser import get_product_table
from .api.scraper import get_product_api_response
from .utils.eventloopwrapper import run_in_loop_async, run_in_loop_sync


# TODO add exceptions and example to doc https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
# TODO logging instead of print
# TODO separate sync/async modules

# TODO complete packaging
# https://docs.astral.sh/uv/guides/package/
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://www.pyopensci.org/python-package-guide/

async def get_products_from_url_async(url: str, refresh: bool = False) -> DataFrame:
    """ Get product tables from a given McMaster-Carr URL

    Parameters
    ----------
    url : str
        The URL to scrape. Must be a valid McMaster-Carr URL. The product tables must be visible on the webpage.
    refresh : bool, optional
        Whether to refresh the cached product table.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the product table.
    """
    cache = dc.Cache(eviction_policy="least-recently-used")
    key = hashlib.md5(url.encode()).hexdigest()

    json = cache.get(key)

    if refresh or not isinstance(json, dict):
        json = await run_in_loop_async(get_product_api_response(url))
        cache.set(key, json)

    return get_product_table(json)


def get_products_from_url(url: str, refresh: bool = False) -> DataFrame:
    return run_in_loop_sync(get_products_from_url_async(url, refresh))
