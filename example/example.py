from mcmaster_scraper.sync_api import get_products_from_url


def main():
    url = "https://www.mcmaster.com/products/springs/extension-springs-1~/system-of-measurement~inch"
    data = get_products_from_url(url)

    stretch_length = 6
    min_force = 10
    max_force = 10.5

    length = data[data.columns[2]]
    extended_length = data[data.columns[5]]
    spring_rate = data[data.columns[8]]

    displacement = stretch_length - length
    force = spring_rate * displacement

    filtered = data[
        (length < stretch_length) &
        (stretch_length < extended_length) &
        (force.between(min_force, max_force))
    ]
    return filtered[["Part Number", "Price"]]


if __name__ == "__main__":
    print(main())
