from mcmaster_scraper.sync_api import get_products_from_url
import pandas as pd


def main():
    url = "https://www.mcmaster.com/products/springs/extension-springs-1~/system-of-measurement~inch"
    data = get_products_from_url(url)

    stretch_length = 0.4
    min_force = 0.5
    max_force = 1

    length = pd.to_numeric(data[data.columns[2]])
    extended_length = pd.to_numeric(data[data.columns[5]])
    spring_rate = pd.to_numeric(data[data.columns[8]])

    displacement = stretch_length - length
    force = spring_rate * displacement

    filtered = data[
        (length < stretch_length) &
        (stretch_length < extended_length) &
        (force.between(min_force, max_force))
    ]
    return filtered


if __name__ == "__main__":
    print(main())
