import diskcache as dc
import hashlib
from pandas import DataFrame

from .api.tableparser import get_product_table
from .api.scraper import get_product_api_response
from .utils.ipykernelpatch import patch_ipykernel

cache = dc.Cache(eviction_policy="least-recently-used")

async def get_products_from_url(url: str, refresh: bool = False) -> DataFrame:
    """ Get product tables from a given URL

    Parameters
    ----------
    url : str
        The url to scrape. Must be a valid McMaster-Carr URL. The product tables must be visible on the webpage.
    refresh : bool, optional
        Whether to refresh the cached product table.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the product table.

    Raises
    ------
    RuntimeError
        If the function is run from a Jupyter notebook and the kernel requires a restart to execute successfully.

    Notes
    -----
    This function uses Playwright under the hood.
    While Playwright is usually incompatible with Jupyter notebooks,
    this function applies a patch to ipykernel under the hood to allow interoperability.
    The patch may require a kernel restart, in which case a RuntimeError will be raised as a notification.

    Examples
    --------
    """
    patch_ipykernel()
    key = _url_to_cache_key(url)
    json = cache.get(key)
    if refresh or not isinstance(json, dict):
        try:
            json = await get_product_api_response(url)
        except NotImplementedError:
            patch_ipykernel()
            raise RuntimeError("Restart kernel required") from None
        cache.set(key, json)

    return get_product_table(json)

def _url_to_cache_key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()
