import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from numpy import nan_to_num

from dash.development.base_component import Component


class EnhancedTable(dbc.Table):
    @classmethod
    def _clean_header_names(cls, x):
        return x.replace('_', ' ').title()

    @classmethod
    def from_dataframe(cls,
                       _df,
                       columns=None,
                       link_column_suffix='_HREF',
                       cell_style_dict=None,
                       **table_kwargs):
        """make a dash table from a pandas dataframe but add hyperlinks based on matching column names. Conditionally style a column or columns
        
        cell_style_dict: dict of {column_name: {condition: style_dict}}
        
        condition can be astring or a function that returns a boolean

        if condition is a string, it must match the value of the column exactly. 
        
        """
        if _df.empty:
            return cls()
        if columns is None:
            columns = _df.columns
        data_dict = _df[columns].to_dict(orient='records')

        col_names = list(data_dict[0].keys())
        header_column_cells = [
            html.Th(cls._clean_header_names(x)) for x in col_names
            if not x.endswith(link_column_suffix)
        ]
        table_header = [html.Thead(html.Tr(header_column_cells))]
        table_body = [
            html.Tbody([
                EnhancedTable._make_row(x,
                                        col_names,
                                        link_column_suffix,
                                        cell_style_dict=cell_style_dict)
                for x in data_dict
            ])
        ]
        return cls(table_header + table_body, **table_kwargs)

    @classmethod
    def _make_row(
        cls,
        data_dict_entry,
        col_names,
        link_column_suffix,
        cell_style_dict=None,
    ):
        if cell_style_dict is None:
            cell_style_dict = {}

        def process_table_cell(col_name, link_names):
            """Add links to tables in the right way and handle nan strings."""
            style = None
            if cell_style_entry := cell_style_dict.get(col_name):
                if isinstance(cell_style_entry[0], list):

                    if data_dict_entry[col_name] in cell_style_entry[0]:
                        style = cell_style_entry[1]
                elif callable(cell_style_entry[0]):
                    if cell_style_entry[0](data_dict_entry[col_name]):
                        style = cell_style_entry[1]

            if (thehref := f"{col_name}{link_column_suffix}") in link_names:

                if data_dict_entry[thehref].startswith("http"):
                    return html.Td(html.A(
                        str(data_dict_entry[col_name]),
                        href=str(data_dict_entry[thehref]),
                    ),
                                   style=style)
                return html.Td(
                    dcc.Link(
                        str(data_dict_entry[col_name]),
                        href=str(data_dict_entry[thehref], style=style),
                    ))
            elif isinstance(data_dict_entry[col_name], float):
                return str(int(nan_to_num(data_dict_entry[col_name])))
            return html.Td(str(data_dict_entry[col_name]), style=style)

        link_names = [x for x in col_names if x.endswith(link_column_suffix)]
        return html.Tr([
            process_table_cell(x, link_names) for x in col_names
            if not x.endswith(link_column_suffix)
        ])
