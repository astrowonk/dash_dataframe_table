from dash import dcc, html, ALL

import dash_bootstrap_components as dbc
from numpy import nan_to_num
import pandas as pd


def _clean_header_names(x):
    if isinstance(x, str):
        return x.replace('_', ' ').title()
    return x


def enhanced_from_dataframe(cls,
                            df,
                            columns=None,
                            link_column_suffix='_HREF',
                            cell_style_dict=None,
                            float_format='.2f',
                            index=False,
                            index_label=None,
                            date_format=None,
                            header_callable=None,
                            link_target=None,
                            button_columns=None,
                            markdown_columns=None,
                            **table_kwargs):
    """make a dash table from a pandas dataframe but add hyperlinks based on matching column names. Conditionally style a column or columns
    
    cell_style_dict: dict of {column_name: {condition: style_dict}}
    
    condition can be astring or a function that returns a boolean

    if condition is a string, it must match the value of the column exactly. 
    
    """
    if df.empty:
        return cls()
    if index:
        df = df.reset_index()
        if index_label is not None:
            df = df.rename(columns={"index": index_label})

    if date_format is not None:
        for c in df.select_dtypes(["datetime"]).columns:
            df[c] = pd.to_datetime(df[c])

    if columns is not None:
        # needed in case columns keyword would otherwise remove  out the link column
        column_order_dict = {key: val for val, key in enumerate(columns)}
        columns = sorted(set(
            list(columns) +
            [f"{col + link_column_suffix}"
             for col in df.columns]).intersection(set(df.columns)),
                         key=lambda x: column_order_dict.get(x, float('inf')))
    else:
        columns = df.columns
    data_dict = df[columns].to_dict(orient='records')

    col_names = list(data_dict[0].keys())
    if header_callable is None:
        header_column_cells = [
            html.Th(_clean_header_names(x)) for x in col_names
            if not str(x).endswith(link_column_suffix)
        ]
    else:
        assert callable(header_callable), "header_callable must be callable"
        header_column_cells = [
            html.Th(header_callable(_clean_header_names(x))) for x in col_names
            if not str(x).endswith(link_column_suffix)
        ]
    table_header = [html.Thead(html.Tr(header_column_cells))]
    table_body = [
        html.Tbody([
            _make_row(x,
                      col_names,
                      link_column_suffix,
                      cell_style_dict=cell_style_dict,
                      float_format=float_format,
                      date_format=date_format,
                      link_target=link_target,
                      button_columns=button_columns,
                      markdown_columns=markdown_columns) for x in data_dict
        ])
    ]
    return cls(table_header + table_body, **table_kwargs)


def _make_row(data_dict_entry,
              col_names,
              link_column_suffix,
              cell_style_dict=None,
              float_format='.2f',
              date_format=None,
              link_target=None,
              button_columns=None,
              markdown_columns=None):
    if button_columns is None:
        button_columns = []
    if markdown_columns is None:
        markdown_columns = []

    if link_target is None:
        link_target = ''
    if cell_style_dict is None:
        cell_style_dict = {}

    def process_table_cell(
        col_name,
        link_names,
    ):
        """Add links to tables in the right way and handle nan strings."""
        style = {}
        if cell_style_entry := cell_style_dict.get(col_name):
            if isinstance(cell_style_entry, list):
                for item in cell_style_entry:
                    if data_dict_entry[col_name] in item[0]:
                        style = item[1]

            elif callable(cell_style_entry):
                if theStyle := cell_style_entry(data_dict_entry):
                    assert isinstance(
                        theStyle,
                        dict), "cell_style Callable must return a dictionary"
                    style = theStyle
            else:
                style = {}
        if (thehref := f"{col_name}{link_column_suffix}") in link_names:

            if data_dict_entry[thehref].startswith("http"):
                return html.Td(
                    html.A(
                        str(data_dict_entry[col_name]),
                        target=link_target,
                        href=str(data_dict_entry[thehref]),
                    ),
                    style=style,
                    className=style.get('className'),
                )
            return html.Td(
                dcc.Link(
                    str(data_dict_entry[col_name]),
                    href=str(data_dict_entry[thehref],
                             style=style,
                             className=style.get('className')),
                ))
        elif col_name in button_columns:
            return html.Td(
                dbc.Button(data_dict_entry[col_name].title(),
                           id={
                               'type': f'{col_name}-button',
                               'index': data_dict_entry[col_name]
                           },
                           color='link'), )
        elif col_name in markdown_columns:
            return html.Td(dcc.Markdown(data_dict_entry[col_name]), )
        elif isinstance(data_dict_entry[col_name], float):
            return html.Td(
                f"{nan_to_num(data_dict_entry[col_name]):{float_format}}",
                style=style,
                className=style.get('className'))
        elif date_format and isinstance(data_dict_entry[col_name],
                                        pd.Timestamp):

            return html.Td(data_dict_entry[col_name].strftime(date_format),
                           style=style,
                           className=style.get('className'))
        return html.Td(str(data_dict_entry[col_name]),
                       style=style,
                       className=style.get('className'))

    link_names = [x for x in col_names if str(x).endswith(link_column_suffix)]
    return html.Tr([
        process_table_cell(x, link_names) for x in col_names
        if not str(x).endswith(link_column_suffix)
    ])


dbc.Table.from_enhanced_dataframe = classmethod(enhanced_from_dataframe)
