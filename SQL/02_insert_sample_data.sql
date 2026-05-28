INSERT INTO public.customers (customer_id, customer_name, segment, region, signup_date) VALUES
    (1, 'Apex Retail Group', 'Enterprise', 'North', '2024-01-12'),
    (2, 'Brightway Services', 'Mid-Market', 'South', '2024-02-03'),
    (3, 'Cobalt Manufacturing', 'Enterprise', 'West', '2024-02-25'),
    (4, 'Delta Health Partners', 'Mid-Market', 'East', '2024-03-19'),
    (5, 'Evergreen Logistics', 'SMB', 'North', '2024-04-08'),
    (6, 'Futura Finance', 'Enterprise', 'East', '2024-04-21'),
    (7, 'Granite Labs', 'SMB', 'West', '2024-05-11'),
    (8, 'Harbor Foods', 'Mid-Market', 'South', '2024-05-29');

INSERT INTO public.products (product_id, product_name, category, unit_price) VALUES
    (1, 'Revenue Intelligence Suite', 'Analytics', 18000.00),
    (2, 'Customer Retention Module', 'Analytics', 9500.00),
    (3, 'Pipeline Forecasting Add-on', 'Forecasting', 12500.00),
    (4, 'Sales Productivity Pack', 'Operations', 7200.00);

INSERT INTO public.sales_reps (rep_id, rep_name, team, region) VALUES
    (1, 'Maya Chen', 'Enterprise', 'North'),
    (2, 'Jordan Smith', 'Growth', 'South'),
    (3, 'Priya Patel', 'Enterprise', 'West'),
    (4, 'Andre Johnson', 'Growth', 'East');

INSERT INTO public.orders (order_id, customer_id, product_id, rep_id, order_date, quantity, discount, revenue) VALUES
    (1001, 1, 1, 1, '2025-01-15', 1, 0.0500, 17100.00),
    (1002, 2, 2, 2, '2025-01-22', 2, 0.0000, 19000.00),
    (1003, 3, 3, 3, '2025-02-08', 1, 0.1000, 11250.00),
    (1004, 4, 4, 4, '2025-02-19', 3, 0.0500, 20520.00),
    (1005, 5, 2, 1, '2025-03-03', 1, 0.0000, 9500.00),
    (1006, 6, 1, 4, '2025-03-17', 2, 0.0800, 33120.00),
    (1007, 7, 4, 3, '2025-04-06', 2, 0.0000, 14400.00),
    (1008, 8, 3, 2, '2025-04-26', 1, 0.0300, 12125.00),
    (1009, 1, 3, 1, '2025-05-09', 2, 0.0500, 23750.00),
    (1010, 3, 1, 3, '2025-05-20', 1, 0.0000, 18000.00),
    (1011, 6, 2, 4, '2025-06-04', 2, 0.0500, 18050.00),
    (1012, 2, 4, 2, '2025-06-18', 4, 0.1000, 25920.00);

INSERT INTO public.opportunities (opportunity_id, customer_id, rep_id, created_date, stage, estimated_value, is_won) VALUES
    (2001, 1, 1, '2025-01-05', 'Closed Won', 24000.00, true),
    (2002, 2, 2, '2025-01-18', 'Closed Won', 19000.00, true),
    (2003, 3, 3, '2025-02-02', 'Negotiation', 32000.00, false),
    (2004, 4, 4, '2025-02-11', 'Proposal', 21000.00, false),
    (2005, 5, 1, '2025-03-01', 'Closed Lost', 9000.00, false),
    (2006, 6, 4, '2025-03-13', 'Closed Won', 33000.00, true),
    (2007, 7, 3, '2025-04-01', 'Discovery', 15000.00, false),
    (2008, 8, 2, '2025-04-21', 'Proposal', 12500.00, false),
    (2009, 1, 1, '2025-05-03', 'Negotiation', 25000.00, false),
    (2010, 6, 4, '2025-06-01', 'Closed Won', 18000.00, true);

INSERT INTO public.sales_activities (activity_id, opportunity_id, activity_date, activity_type) VALUES
    (3001, 2001, '2025-01-06', 'Discovery Call'),
    (3002, 2001, '2025-01-10', 'Proposal Sent'),
    (3003, 2002, '2025-01-20', 'Demo'),
    (3004, 2003, '2025-02-05', 'Executive Meeting'),
    (3005, 2004, '2025-02-13', 'Proposal Sent'),
    (3006, 2006, '2025-03-15', 'Contract Review'),
    (3007, 2007, '2025-04-04', 'Discovery Call'),
    (3008, 2008, '2025-04-24', 'Demo'),
    (3009, 2009, '2025-05-07', 'Negotiation'),
    (3010, 2010, '2025-06-03', 'Contract Signed');
