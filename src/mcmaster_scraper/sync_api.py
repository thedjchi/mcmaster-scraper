from pandas import DataFrame

from .async_api import get_products_from_url as get_products_from_url_async
from ._utils.event_loop_wrapper import run_in_loop_sync


def get_products_from_url(url: str, refresh: bool = False) -> DataFrame:
    return run_in_loop_sync(get_products_from_url_async(url, refresh))