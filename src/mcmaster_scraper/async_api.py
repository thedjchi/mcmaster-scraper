import diskcache as dc
import hashlib

import platformdirs
from pandas import DataFrame

from ._api.table_parser import get_product_table
from ._api.scraper import get_product_api_response
from ._utils.event_loop_wrapper import run_in_loop_async


# TODO add exceptions and example to doc https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
# TODO logging instead of print

# TODO complete packaging
# https://docs.astral.sh/uv/guides/package/
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://www.pyopensci.org/python-package-guide/

async def get_products_from_url(url: str, refresh: bool = False) -> DataFrame:
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
    cache_dir = platformdirs.user_cache_dir("mcmaster_scraper", None)
    cache = dc.Cache(cache_dir, eviction_policy="least-recently-used")
    key = hashlib.md5(url.encode()).hexdigest()

    if key in cache and not refresh:
        json = cache[key]
    else:
        json = await run_in_loop_async(get_product_api_response(url))
        cache[key] = json

    return get_product_table(json)
