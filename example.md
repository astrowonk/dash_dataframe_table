
### Conditional Formatting and Automatic hyperlinks


[EnhancedTable](https://github.com/astrowonk/dash_dataframe_table) will automatically generate `dcc.Link` or `html.A` wrappers around a column from a __matched column in the same dataframe__.  The hyperlink column must match the column_name + a specific suffix. In the example to the right, the (hidden) link column is `Company_HREF`, using the default suffix.

I originally built a variant of this so I could navigate to other parts of my multipage app via a table. You can seen this in action on most tables of bills and legislators at [Recorded Vote](https://recordedvote.org) such as linking to the legislators pages by name on the [vote history pages](https://recordedvote.org/history_event/201/HV1578). 

Conditional Formatting criteria can either be a list of tuples `(match_list,style_dict)` or a `callable` that returns the style dict if the condition is met. This allows for more complex condition formatting.

The code below generates the conditional formatting you see. You can also add a specific bootstrap class by putting a `className` key in the "style" dictionary.

```python

def color_positive(x):
    val = x['Value2']
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
```

