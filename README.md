# McMaster-Scraper
A Python library for fetching product tables from a McMaster-Carr URL as a DataFrame for complex filtering and calculations.

## Features
- Asynchronous API compatible with both Python files and Jupyter notebooks
- Caches data locally to speed up subsequent calls

## Setup
`pip install mcmaster-parser`

## Usage
```
data = await get_products_from_url(url: str, refresh: bool = False)
```
Fetches all parts on a given McMaster page and returns the result as a DataFrame.

**IMPORTANT:** The product tables **MUST** be visible on the webpage for the call to succeed. If needed, you should specify some filters in McMaster to narrow the search pool so that the product tables will be visible.

## License
[MIT](LICENSE)