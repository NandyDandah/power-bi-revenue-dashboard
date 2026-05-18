# Sales Rep Performance Dashboard

Use this as a fourth report page after the existing `Sales Funnel` page.

## Page Setup

- Page name: `Sales Rep Performance`
- Canvas: 16:9, 1280 x 720
- Theme: import either `Project Assets/Themes/Revenue_Dashboard_Light.json` or `Project Assets/Themes/Revenue_Dashboard_Dark.json`
- Required relationship: `Date[Date]` to `'public orders'[order_date]`
- Primary slicers: `Date[Year Month]`, `'public sales_reps'[rep_name]`, `'public customers'[region]`, `'public opportunities'[stage]`

## Top KPI Row

Add five card visuals across the top:

- `Total Revenue`
- `Revenue MoM %`
- `Total Pipeline Value`
- `Opportunity Win Rate`
- `Average Order Value`

Format percentage cards as percentage with one decimal place. Use conditional formatting:

- Positive trend: green
- Neutral or zero: amber
- Negative trend: red

## Main Visuals

1. Clustered bar chart: `Total Revenue` by `'public sales_reps'[rep_name]`
   - Sort descending by `Total Revenue`
   - Add `Rep Revenue Rank` as tooltip

2. Line chart: `Total Revenue`, `Revenue Previous Year`, and `Revenue MoM %` by `Date[Year Month]`
   - Use continuous monthly trend if the model supports it
   - Show secondary axis for `Revenue MoM %`

3. Matrix: `'public sales_reps'[rep_name]` rows with:
   - `Total Revenue`
   - `Revenue Share by Rep`
   - `Total Orders`
   - `Average Order Value`
   - `Opportunity Win Rate`
   - `Total Pipeline Value`
   - `Rep Performance Tier`

4. Scatter chart: rep quality map
   - X axis: `Opportunity Win Rate`
   - Y axis: `Average Order Value`
   - Size: `Total Revenue`
   - Legend/details: `'public sales_reps'[rep_name]`

5. Donut or treemap: `Total Pipeline Value` by `'public opportunities'[stage]`
   - Add `Open Opportunities` and `Pipeline per Open Opportunity` as tooltips

## Drill and Tooltip Ideas

- Enable drillthrough by `'public sales_reps'[rep_name]` for a dedicated rep detail page.
- Tooltip fields for rep visuals: `Revenue YTD`, `Revenue YoY %`, `Revenue MoM %`, `Revenue Share by Rep`, `Pipeline Share by Rep`.
- Use `Rep Performance Tier` as a matrix column or conditional label.

## Recommended Page Flow

1. `Page 1`: executive revenue overview
2. `Customer Retention`: retention and active customer health
3. `Sales Funnel`: pipeline and opportunity conversion
4. `Sales Rep Performance`: individual rep contribution and trend performance
