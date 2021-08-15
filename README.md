
## Links in Dash Bootstrap dataframes

I need to be able to easily create hyperlinks for a table from dataframe, the easiest way being based on another column in the same dataframe. This will wrap `column` in the link from `column_HREF` by default. You can specify a different suffix.

This is still a work in progress. The new method doesn't quite have the same functionality or keywords as the original yet, such as `header`. The conditional formatting is nice but doesn't extend to multiple criteria in the same column.

## Live Examples

The [example.py file is running live on my site](https://marcoshuerta.com/dash/table_example/)

## Installation

setup.py installs an egg which was causing dash to crash when debugging for reasons I can't explain. So clone and do the `pip install .` tric

```
git clone https://github.com/astrowonk/dash_dataframe_table.git
cd dash_dataframe_table
pip install .
```

You can run example.py app without install via pip or setup if you like.

```
git clone https://github.com/astrowonk/dash_dataframe_table.git
cd dash_dataframe_table
python example.py
```


### Usage, Examples

The `example.py` dash app shows it in action, both adding links automatically to the company column name, and styling the columns conditionally.

I'm still debating if I should just monkey patch a new method onto `dbc.Table` or just subclass it as I've done here.

The company column is given hyperlinks from a midden `Company_HREF` column. See the `example.py` dash app code for more.

The method on this class also supports conditional style formatting. This can either be a list of matching values, or a callable that returns a boolean. 

```python

def color_positive(val):

    if val > 0:
        return {'className': 'table-success'}
    elif val < 0:
        return {'className': "table-warning"}

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

html.Div(
            EnhancedTable.from_dataframe(df, striped=True, cell_style_dict=my_style_dict)
        )
```

