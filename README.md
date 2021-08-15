
## Links in Dash Bootstrap dataframes

I need to be able to easily create hyperlinks for a table from dataframe, the easiest way being based on another column in the same dataframe. This will wrap `column` in the link from `column_HREF` by default. You can specify a different suffix.

Still a work in progress, I need to get setup.py and such working.

The example.py shows it in action, both adding links automatically to the company column name, and styling the columns conditionally.

Hyperlinks on one column. Conditional bold formatting on Company, using a callable to style the Value columns.

![Screen Shot 2021-08-15 at 12 27 12 AM](https://user-images.githubusercontent.com/13702392/129467178-b71e30fb-723e-413e-9e0f-57d657c3f3a6.png)
