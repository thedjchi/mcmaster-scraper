# McMaster-Scraper

A Python library for fetching product tables from a McMaster-Carr URL as a DataFrame for complex filtering and
calculations.

## Features

- Caches data locally to speed up future calls
- Supports both sync/async APIs
- Works in Python files and Jupyter notebooks
- Includes convenience functions to quickly retrieve product tables from multiple URLs
- Typed functions for type-checking compatibility

## Setup

McMaster-Scraper is available on PyPi:

`pip install mcmaster-scraper`

McMaster-Scraper requires Playwright to fetch the product tables. It is already included as a dependency. However, you will need to install the browsers manually:

`playwright install`

## Usage

### Imports

```
# SYNC API
from mcmaster_scraper.sync_api import get_products_from_url

# ASYNC API
from mcmaster_scraper.async_api import get_products_from_url
```

### get_products_from_url
`def get_products_from_url(url: str, refresh: bool = False) -> DataFrame`

Gets product tables from a given McMaster-Carr URL.

If there are multiple product tables, they will be merged, and an additional "Product Type" column will be added.

**Parameters:**

    url : str
        The URL to scrape. Must be a valid McMaster-Carr URL. The product tables must be visible on the webpage.

    refresh : bool, optional
        Whether to refresh the cached data. Default is `False`.

**Returns:**

    DataFrame
        A pandas DataFrame containing the combined product tables.

**Raises:**

    ValueError
        If the URL is not a valid McMaster-Carr URL.

### get_products_from_urls
`def get_products_from_urls(urls: list[str], refresh: bool = False) -> list[DataFrame]`

Gets product tables from a list of McMaster-Carr URLs.

**See Also:**

`get_products_from_url`

## Disclaimer

This library is for authorized data extraction only. Do not:

- Scrape beyond reasonable rates
- Violate Terms of Service
- Circumvent access controls
- Use data for unauthorized commercial purposes

## Legal Notice

This library is provided as-is. Authors are not liable for any legal, technical, or business consequences resulting from
misuse of this library. Users assume full responsibility for compliance with applicable laws, regulations, and website
policies.

**By using this library, you acknowledge and agree to these responsibilities.**

## License

[MIT](LICENSE)