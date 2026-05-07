from pandas import DataFrame
from ._text_parser import get_header_text, get_cell_text

def get_product_tables(json: dict) -> dict[str, DataFrame]:
    tables = _find_pivot_tables(json)
    dataframes = { k: _parse_pivot_table(v) for k, v in tables.items() }
    return dataframes


# TODO iterate over all tables
def _find_pivot_tables(root: dict) -> dict:
    stack = [root]
    while stack:
        node = stack.pop()

        if isinstance(node, dict):
            if node.get("Name") == "ProductPresentations":
                return { product["Display"]["Title"]: product["Table"] for product in node["Data"] }
            else:
                stack.extend(node.values())

        elif isinstance(node, list):
            stack.extend(node)

    raise IOError("The McMaster URL provided does not have a visible product table.")


def _parse_pivot_table(table: dict) -> DataFrame:
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
