# Revenue Performance Dashboard

Power BI portfolio project exploring revenue performance, customer retention, sales pipeline, and sales representative contribution. Four report pages use a consistent KPI strip, aligned chart grid, and dedicated filter area.

**Power BI | DAX | PostgreSQL | Sales analytics**

## Expanded Demonstration Dataset

The report contains **2,232 orders, 120 customers, eight sales representatives, 1,080 opportunities and 3,240 activities** across January 2024 to December 2025. All records are synthetic portfolio data, not actual business results. Run `python advance_project.py` to reproduce the embedded tables and SQL seed data.

Monthly revenue charts show seasonality across 24 months. The executive page also compares revenue by product and customer segment. Pipeline measures exclude closed opportunities; lost deals count only Closed Lost records. The $65 million revenue target is a demonstration assumption for the full dataset, not an approved business budget.

The legacy retention metric represents the share of current-month customers who also ordered in the previous month. It is not cohort retention. Monthly Active Customers shows the average monthly count across the selected summary months. Monthly summary tables are pre-aggregated and do not respond to customer or rep filters.

The expanded model still requires a refresh and visual verification in Power BI Desktop. Existing screenshots predate this data expansion.

The editable report uses embedded demonstration data. PostgreSQL scripts are included separately for reviewing the database design. GitHub displays static images; open the complete PBIP project in Power BI Desktop to interact with the report.

## Project Contents

- `Power BI Project.pbip` - publish-ready editable Power BI Project file.
- `Power BI Project.Report/` - report page and visual definitions.
- `Power BI Project.SemanticModel/` - semantic model, relationships, tables, and DAX measures.
- `SQL/` - PostgreSQL setup scripts for tables, sample data, and reporting views.
- `screenshots/` - dashboard page previews for GitHub and recruiter review.
- `PROJECT_SKILLS.md` - portfolio summary for recruiters and hiring managers.

## Illustrative Previews

These existing images are illustrative portfolio previews, not screenshots of the current Power BI report. The updated report layout must be refreshed and captured in Power BI Desktop before replacing them with verified screenshots.

![Executive Overview](screenshots/executive-overview.png)

![Customer Retention](screenshots/customer-retention.png)

![Sales Funnel](screenshots/sales-funnel.png)

![Sales Rep Performance](screenshots/sales-rep-performance.png)

## Dashboard Pages

- Executive Overview
- Customer Retention
- Sales Funnel
- Sales Rep Performance

## Features

- Revenue, orders, active customers, conversion, and average order value KPIs
- Customer retention and monthly active customer analysis
- Opportunity funnel and pipeline tracking
- Advanced DAX measures for MTD, QTD, YTD, MoM, QoQ, and YoY trends
- Sales representative ranking, contribution share, and performance scoring
- Recruiter-friendly PBIP source structure with report and semantic model files
- PostgreSQL schema, seed data, and views included for reproducible setup

## Skills Demonstrated

- Power BI report design and page layout
- DAX KPI development and time intelligence
- Semantic model relationships and measure organization
- PostgreSQL table/view design for analytics reporting
- Sales analytics, retention analysis, and pipeline reporting
- GitHub-ready project packaging and documentation

## How To Review

1. Download the complete repository and open `Power BI Project.pbip` in Power BI Desktop. Keep the Report and SemanticModel folders beside it.
2. Review the four report pages and the `Revenue_measures` table.
3. Refresh and inspect all four pages in Desktop before publishing to your Power BI workspace.
4. Read `PROJECT_SKILLS.md` for a concise portfolio explanation.

## PostgreSQL Setup

Run the SQL scripts in order if you want to recreate the source database:

1. `SQL/01_create_tables.sql`
2. `SQL/02_insert_sample_data.sql`
3. `SQL/03_create_views.sql`

## Tools

- Power BI Desktop
- DAX
- PostgreSQL
- Power BI JSON themes
- Git/GitHub
