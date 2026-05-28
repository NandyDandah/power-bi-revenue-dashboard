CREATE OR REPLACE VIEW public.vw_revenue_trends AS
SELECT
    date_trunc('month', order_date)::date AS month,
    SUM(revenue)::numeric(14, 2) AS total_revenue,
    COUNT(*)::integer AS total_orders,
    COUNT(DISTINCT customer_id)::integer AS active_customers,
    ROUND((SUM(revenue) / NULLIF(COUNT(*), 0))::numeric, 2) AS avg_order_value
FROM public.orders
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE VIEW public.vw_customer_retention AS
WITH monthly_customers AS (
    SELECT DISTINCT
        date_trunc('month', order_date)::date AS order_month,
        customer_id
    FROM public.orders
),
retention AS (
    SELECT
        current_month.order_month,
        COUNT(DISTINCT current_month.customer_id)::integer AS active_customers,
        COUNT(DISTINCT prior_month.customer_id)::integer AS retained_customers
    FROM monthly_customers current_month
    LEFT JOIN monthly_customers prior_month
        ON prior_month.customer_id = current_month.customer_id
        AND prior_month.order_month = current_month.order_month - INTERVAL '1 month'
    GROUP BY current_month.order_month
)
SELECT
    order_month,
    active_customers,
    retained_customers,
    COALESCE(retained_customers::numeric / NULLIF(active_customers, 0), 0)::double precision AS retention_rate
FROM retention
ORDER BY order_month;

CREATE OR REPLACE VIEW public.vw_sales_funnel AS
SELECT
    stage,
    COUNT(*)::integer AS opportunity_count,
    SUM(estimated_value)::numeric(14, 2) AS pipeline_value,
    SUM(CASE WHEN is_won THEN 1 ELSE 0 END)::integer AS won_count,
    COALESCE(SUM(CASE WHEN is_won THEN 1 ELSE 0 END)::numeric / NULLIF(COUNT(*), 0), 0)::double precision AS stage_win_rate
FROM public.opportunities
GROUP BY stage
ORDER BY pipeline_value DESC;

CREATE OR REPLACE VIEW public.vw_rep_performance AS
SELECT
    reps.rep_name,
    reps.team,
    reps.region,
    COUNT(orders.order_id)::integer AS total_orders,
    COALESCE(SUM(orders.revenue), 0)::numeric(14, 2) AS total_revenue,
    ROUND((COALESCE(SUM(orders.revenue), 0) / NULLIF(COUNT(orders.order_id), 0))::numeric, 2) AS avg_order_value,
    COUNT(DISTINCT orders.customer_id)::integer AS unique_customers
FROM public.sales_reps reps
LEFT JOIN public.orders orders
    ON orders.rep_id = reps.rep_id
GROUP BY reps.rep_name, reps.team, reps.region
ORDER BY total_revenue DESC;

CREATE OR REPLACE VIEW public.vw_kpi_summary AS
SELECT
    SUM(revenue)::numeric(14, 2) AS total_revenue,
    COUNT(*)::integer AS total_orders,
    COUNT(DISTINCT customer_id)::integer AS active_customers,
    ROUND((SUM(revenue) / NULLIF(COUNT(*), 0))::numeric, 2) AS avg_order_value,
    (SELECT COUNT(*) FROM public.opportunities)::integer AS total_opportunities,
    (SELECT COUNT(*) FROM public.opportunities WHERE is_won)::integer AS won_opportunities,
    (
        SELECT COALESCE((COUNT(*) FILTER (WHERE is_won))::numeric / NULLIF(COUNT(*), 0), 0)
        FROM public.opportunities
    )::double precision AS conversion_rate
FROM public.orders;
