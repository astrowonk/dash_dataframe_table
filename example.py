import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from dash_dataframe_table import EnhancedTable

app = dash.Dash("example of dataframe",
                external_stylesheets=[dbc.themes.YETI],
                title="Example Data Frame",
                meta_tags=[
                    {
                        "name": "viewport",
                        "content": "width=device-width, initial-scale=1"
                    },
                ])

the_list = [
    "Apple", "Google", "Yahoo", "Facebook", "Microsoft", "Amazon", "IBM",
    "Intel", "Oracle", "Intel"
]

start_date = datetime.datetime(2018, 1, 1)
date_list = pd.date_range(start_date, periods=len(the_list)).tolist()

## make a simple dataframe with links

df = pd.DataFrame([{
    'Company': x,
    "Company_HREF": f"https://{x.lower()}.com",
    "Value": (n - 4) / 13,
    "Date": date_list[n]
} for n, x in enumerate(the_list)])

## make the conditional styling dictionary
my_style_dict = {
    'Company': (['Yahoo', 'Apple'], {
        'font-weight': 'bold'
    }),
    'Value': (lambda x: x > 0, {
        'background-color': '#7FFFD4'
    })
}

app.layout = dbc.Container(
    [
        html.H4('Example Table from Dataframe'),
        ### maybe it shouldn't return a dbc table but rather the elemnts of the table so one can choose dbc or dcc
        html.Div(
            EnhancedTable.from_dataframe(df,
                                         striped=True,
                                         cell_style_dict=my_style_dict,
                                         id='hello',
                                         float_format='.2f',
                                         date_format='%Y-%m-%d'), )
    ],
    style={'margin-top': '10px'})

if __name__ == "__main__":
    app.run_server(debug=True)
