
## Links in Dash Bootstrap dataframes

I need to be able to easily create hyperlinks for a table from dataframe, the easiest way being based on another column in the same dataframe. This will wrap `column` in the link from `column_HREF` by default. You can specify a different suffix.

This is still a work in progress. The new method doesn't quite have the same functionality or keywords as the original yet, such as `header`. The conditional formatting is nice but doesn't extend to multiple criteria in the same column.

The `example.py` dash app shows it in action, both adding links automatically to the company column name, and styling the columns conditionally.

I'm still debating if I should just monkey patch a new method onto `dbc.Table` or just subclass it as I've done here.

### Usage, Examples

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


### Screenshots

#### Dataframe in Jupyter

![Screen Shot 2021-08-15 at 9 31 32 AM](https://user-images.githubusercontent.com/13702392/129480284-abe914ae-d5a7-4618-9b73-9c7f3bbd5ff9.png)


#### Rendered table in Dash

![Screen Shot 2021-08-15 at 12 27 12 AM](https://user-images.githubusercontent.com/13702392/129467178-b71e30fb-723e-413e-9e0f-57d657c3f3a6.png)
