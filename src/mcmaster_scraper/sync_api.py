from pandas import DataFrame

from .async_api import get_products_from_url as get_products_from_url_async
from ._utils.event_loop_wrapper import run_in_loop_sync


def get_products_from_url(url: str, refresh: bool = False) -> DataFrame:
    """ Gets product tables from a given McMaster-Carr URL.

        If there are multiple product tables, they will be merged, and an additional "Product" column will be added.

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
    return run_in_loop_sync(get_products_from_url_async(url, refresh))