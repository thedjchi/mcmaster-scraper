# McMaster-Scraper

A Python library for fetching product tables from a [McMaster-Carr](https://www.mcmaster.com) URL
as a [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) for complex filtering and
calculations.

![PyPI - Version](https://img.shields.io/pypi/v/mcmaster-scraper?style=for-the-badge)
![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/mcmaster-scraper?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/mcmaster-scraper?style=for-the-badge)


## Features

- Caches data locally to speed up future calls
- Supports both sync/async APIs
- Works in Python files and Jupyter notebooks
- Includes convenience functions to quickly retrieve product tables from multiple URLs
- Typed functions for type-checking compatibility

## Install

McMaster-Scraper is available on PyPi:

`pip install mcmaster-scraper`

McMaster-Scraper requires [Playwright](https://playwright.dev/python) to fetch the product tables. It is already included as a dependency. However, you will need to install the browsers manually:

`playwright install`

## Quick Start

```
from mcmaster_scraper.sync_api import get_products_from_url

url = "https://www.mcmaster.com/products/screws/socket-head-screws-2~/steel-socket-head-screws~~/"
data = get_products_from_url(url) # Returns a DataFrame with all the products from the URL

... # Do stuff with the DataFrame (filter, perform calculations, etc.)
```

## Docs

### API Reference

The API reference can be found in [GitHub Pages](https://thedjchi.github.io/mcmaster-scraper/mcmaster_scraper.html).

### Examples

An example script can be found in [docs/example.py](docs/example.py).

## Disclaimer

This library is for responsible data extraction only. Do not:

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