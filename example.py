import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from dash_dataframe_table import EnhancedTable

with open("example.md", "r") as myfile:
    markdown_text = myfile.read()

app = dash.Dash("example of dataframe",
                external_stylesheets=[dbc.themes.YETI],
                title="Example Data Frame",
                meta_tags=[
                    {
                        "name": "viewport",
                        "content": "width=device-width, initial-scale=1"
                    },
                ])
server = app.server

the_list = [
    "Apple", "Google", "Yahoo", "Facebook", "Microsoft", "Amazon", "IBM",
    "Intel", "Oracle"
]

start_date = datetime.datetime(2018, 1, 1)
date_list = pd.date_range(start_date, periods=len(the_list)).tolist()

## make a simple dataframe with links

df = pd.DataFrame([{
    'Company': x,
    "Company_HREF": f"https://{x.lower()}.com",
    "Value": (n - 4) / 13,
    "Value2": (n**4) / 13,
    "Date": date_list[n]
} for n, x in enumerate(the_list)])


def color_positive(val):

    if val > 0:
        return {'className': 'table-success'}
    elif val < 0:
        return {'className': "table-warning"}


## make the conditional styling dictionary
cell_style_dict = {
    'Company': [
        (['Yahoo', 'Apple'], {
            'font-weight': 'bold'
        }),
        (['Oracle'], {
            'className': 'table-danger'
        }),
    ],
    'Value2':
    lambda x: {
        'background-color': '#7FFFD4'
    } if x > 10 else {},
    'Date':
    lambda x: {
        'className': 'table-info'
    } if x.weekday() in [4, 6] else {},
    'Value':
    color_positive
}

col_one = dbc.Col(dcc.Markdown(markdown_text), )
col_two = dbc.Col([
    html.H4('Rendered Table from Dataframe'),
    EnhancedTable.from_dataframe(
        df,
        striped=True,
        cell_style_dict=cell_style_dict,
        id='hello',
        float_format='.2f',
        date_format='%Y-%m-%d',
        columns=['Company', 'Date', 'Value', 'Value2']),
])

app.layout = dbc.Container([dbc.Row([col_one, col_two])],
                           style={'margin-top': '10px'})

if __name__ == "__main__":
    app.run_server(debug=True)
