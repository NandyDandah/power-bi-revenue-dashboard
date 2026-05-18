# Power BI Revenue Project Completion Pack

This folder adds the requested completion assets for the existing `Revenue Performance Dashboard.pbix`.

## Included

- `DAX/Advanced_KPI_Time_Intelligence_Measures.dax`: advanced KPI, sales rep performance, and time intelligence measures.
- `Themes/Revenue_Dashboard_Light.json`: importable light Power BI theme.
- `Themes/Revenue_Dashboard_Dark.json`: importable dark Power BI theme.
- `Pages/Sales_Rep_Performance_Dashboard.md`: page blueprint for the new Sales Rep Performance dashboard.

## Apply Order

1. Open `Revenue Performance Dashboard.pbix` in Power BI Desktop.
2. Add the `Date` calculated table from the DAX file.
3. Mark `Date[Date]` as the date table.
4. Create the relationship from `Date[Date]` to `'public orders'[order_date]`.
5. Add the measures from the DAX file to the existing `Revenue_measures` table.
6. Import either the light or dark theme from `View > Browse for themes`.
7. Add the `Sales Rep Performance` page using the layout guide.

## Notes

The current workspace contains a closed `.pbix` file only. Adding model measures directly into a PBIX package requires Power BI Desktop, Tabular Editor, or pbi-tools automation. Those tools were not available in this environment, so the PBIX itself was left untouched and the completion work was added as import-ready project assets.
