import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from numpy import nan_to_num


def _clean_header_names(x):
    return x.replace('_', ' ').title()


def make_table_from_df(
    _df,
    columns=None,
    link_column_suffix='_HREF',
):
    if _df.empty:
        return dbc.Table()
    if columns is None:
        columns = _df.columns
    data_dict = _df[columns].to_dict(orient='records')

    col_names = list(data_dict[0].keys())
    header_column_cells = [
        html.Th(_clean_header_names(x)) for x in col_names
        if not x.endswith('_HREF')
    ]
    table_header = [html.Thead(html.Tr(header_column_cells))]
    table_body = [
        html.Tbody(
            [_make_row(x, col_names, link_column_suffix) for x in data_dict])
    ]
    return dbc.Table(table_header + table_body)


def _make_row(data_dict_entry, col_names, link_column_suffix):
    def process_cell_links(col_name, link_names):
        """Add links to tables in the right way and handle nan strings."""
        if (thehref := f"{col_name}{link_column_suffix}") in link_names:
            return dcc.Link(str(data_dict_entry[col_name]),
                            href=str(data_dict_entry[thehref]))
        elif isinstance(data_dict_entry[col_name], float):
            return str(int(nan_to_num(data_dict_entry[col_name])))
        return str(data_dict_entry[col_name])

    link_names = [x for x in col_names if x.endswith('_HREF')]
    return html.Tr([
        html.Td(process_cell_links(x, link_names)) for x in col_names
        if not x.endswith('_HREF')
    ])
