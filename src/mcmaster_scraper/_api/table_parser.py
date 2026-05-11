from pandas import DataFrame, concat

from ._text_parser import get_cell_text, get_header_text


def get_products_table(json: dict) -> DataFrame:
    tables = _find_pivot_tables(json)
    dataframes = {k: _parse_pivot_table(v) for k, v in tables.items()}
    dataframes_with_product_type = [
        table.assign(**{"Product Type": product})
        for product, table in dataframes.items()
    ]
    return concat(dataframes_with_product_type, ignore_index=True)


def _find_pivot_tables(root: dict) -> dict:
    stack = [root]
    while stack:
        node = stack.pop()

        if isinstance(node, dict):
            if node.get("Name") == "ProductPresentations":
                return {
                    item["Display"]["Title"]: item["Table"]
                    for product in node["Data"]
                    for item in [product, *product["Children"]]
                }
            else:
                stack.extend(node.values())

        elif isinstance(node, list):
            stack.extend(node)

    raise KeyError("The McMaster URL provided does not have a visible product table.")


def _parse_pivot_table(table: dict) -> DataFrame:
    # For tables with multiple products in the same row,
    # only get the columns for the primary product
    col_ids = table["Transformations"]["PrimaryProductGroup"]["ColumnIds"]

    # For tables with only one product per row, PrimaryProductGroup will be empty
    # Fallback to all columns instead
    if len(col_ids) == 0:
        col_ids = table["ColumnIds"]

    rows = table["Rows"]
    meta = table["Metadata"]

    # Build headers
    headers = [get_header_text(col_id, meta) for col_id in col_ids]

    # Build row data
    def get_row_data(row: dict):
        cell_ids = row["ColumnIdToCellIdMap"]
        return {
            header: get_cell_text(cell_ids[col_id], meta)
            for col_id, header in zip(col_ids, headers)
        }

    data = [get_row_data(row) for row in rows]
    return DataFrame(data)
