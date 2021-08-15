
### Conditional Formatting and Automatic hyperlinks


`EnhancedTable` will automatically generate `dcc.Link` or `html.A` wrappers around a column from a __matched column in the same dataframe__.  The hyperlink column must match the column_name + a specific suffix. In the example to the right, the (hidden) link column is `Company_HREF`, using the default suffix.

 I originally built a variant of this so I could navigate to other parts of my multipage app via a table. You can seen this in action on most tables of bills and legislators at [Recorded Vote](https://recordedvote.org) such as linking to the legislators pages by name on the [vote history pages](https://recordedvote.org/history_event/201/HV1578). 

Conditional Formatting comes from the `cell_style_dict` which has the form of `col_name : (criteria,style_dict)`.

Criteria can either be a list of matching values, or a `callable` that returns true if the condition is met.

The code below generates the conditional formatting you see. You can also tag a cell with a specific bootstrap class by putting a `className` key in the "style" dictionary.

```python
cell_style_dict = {
    'Company': (['Yahoo', 'Apple'], {
        'font-weight': 'bold'
    }),
    'Value': (lambda x: x > 0, {
        'background-color': '#7FFFD4'
    }),
    'Date': (lambda x: x.weekday() == 4, {
        'className': 'table-warning'
    }),
}
```

