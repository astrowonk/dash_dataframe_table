import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from numpy import nan_to_num
import pandas as pd


def _clean_header_names(x):
    return x.replace('_', ' ').title()


def enhanced_from_dataframe(cls,
                            df,
                            columns=None,
                            link_column_suffix='_HREF',
                            cell_style_dict=None,
                            float_format='.2f',
                            index=False,
                            index_label=None,
                            date_format=None,
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
    header_column_cells = [
        html.Th(_clean_header_names(x)) for x in col_names
        if not x.endswith(link_column_suffix)
    ]
    table_header = [html.Thead(html.Tr(header_column_cells))]
    table_body = [
        html.Tbody([
            _make_row(x,
                      col_names,
                      link_column_suffix,
                      cell_style_dict=cell_style_dict,
                      float_format=float_format,
                      date_format=date_format) for x in data_dict
        ])
    ]
    return cls(table_header + table_body, **table_kwargs)


def _make_row(data_dict_entry,
              col_names,
              link_column_suffix,
              cell_style_dict=None,
              float_format='.2f',
              date_format=None):
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
                        print(style)

            elif callable(cell_style_entry):
                if theStyle := cell_style_entry(data_dict_entry[col_name]):
                    assert isinstance(
                        theStyle,
                        dict), "cell_style Callable must return a dictionary"
                    style = theStyle
            else:
                style = {}
        if (thehref := f"{col_name}{link_column_suffix}") in link_names:

            if data_dict_entry[thehref].startswith("http"):
                return html.Td(html.A(
                    str(data_dict_entry[col_name]),
                    href=str(data_dict_entry[thehref]),
                ),
                               style=style,
                               className=style.get('className'))
            return html.Td(
                dcc.Link(
                    str(data_dict_entry[col_name]),
                    href=str(data_dict_entry[thehref],
                             style=style,
                             className=style.get('className')),
                ))
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

    link_names = [x for x in col_names if x.endswith(link_column_suffix)]
    return html.Tr([
        process_table_cell(x, link_names) for x in col_names
        if not x.endswith(link_column_suffix)
    ])


dbc.Table.from_enhanced_dataframe = classmethod(enhanced_from_dataframe)
